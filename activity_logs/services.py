import json
import re
from collections.abc import Callable
from typing import Any

from django.http import HttpRequest

from .models import ActivityLog

_SEGMENT_LABELS = {
    "projects": "Updated a project",
    "users": "Updated your account",
    "feedback": "Submitted feedback",
    "notifications": "Updated a notification",
}


def _generic_description(request):
    segments = [s for s in request.path.split("/") if s]
    return _SEGMENT_LABELS.get(segments[0], "Performed an action") if segments else "Performed an action"


def get_client_ip(request: HttpRequest) -> str | None:
    meta = getattr(request, "META", {}) or {}

    forwarded_for = meta.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return meta.get("REMOTE_ADDR")


def log_activity(
    *,
    request: HttpRequest,
    action: str,
    description: str = "",
    user=None,
    status_code: int | None = None,
) -> ActivityLog:
    activity_user = user or getattr(request, "user", None)

    if not getattr(activity_user, "is_authenticated", False):
        activity_user = None

    path = getattr(request, "path", "") or ""
    method = getattr(request, "method", "") or ""

    return ActivityLog.objects.create(
        user=activity_user,
        action=action,
        description=description,
        path=path,
        method=method,
        status_code=status_code,
        ip_address=get_client_ip(request),
    )


def _project_label(project_id):
    """Looks up a project's title for a friendlier description. Falls
    back gracefully if the project is gone or the lookup fails for any
    reason -- this is only ever used for a log message, never critical."""
    try:
        from projects.models import Project

        title = Project.objects.filter(id=project_id).values_list("title", flat=True).first()
    except Exception:
        title = None

    return f"'{title}'" if title else "a project"


def _response_json(response):
    try:
        return json.loads(response.content)
    except Exception:
        return {}


_PATTERNS: list[tuple[re.Pattern[str], Any, Callable[..., Any]]] = []


def register(pattern, methods=None):
    compiled = re.compile(pattern)

    def decorator(handler):
        _PATTERNS.append((compiled, methods, handler))
        return handler

    return decorator


@register(r"^/projects/create-project/$", {"POST"})
def _create_project(request, response, match):
    return ActivityLog.Action.CREATE_PROJECT, "Created a new project"


@register(r"^/projects/(?P<id>\d+)/edit/$", {"POST"})
def _update_project(request, response, match):
    label = _project_label(match.group("id"))
    return ActivityLog.Action.UPDATE_PROJECT, f"Updated project {label}"


@register(r"^/projects/(?P<id>\d+)/delete/$", {"POST"})
def _delete_project(request, response, match):
    label = _project_label(match.group("id"))
    return ActivityLog.Action.DELETE_PROJECT, f"Deleted project {label}"


@register(r"^/projects/(?P<id>\d+)/like/$", {"POST"})
def _like_project(request, response, match):
    liked = _response_json(response).get("liked")
    label = _project_label(match.group("id"))
    if liked is False:
        return ActivityLog.Action.LIKE_PROJECT, f"Removed like from project {label}"
    return ActivityLog.Action.LIKE_PROJECT, f"Liked project {label}"


@register(r"^/projects/(?P<id>\d+)/share-email/$", {"POST"})
def _share_project(request, response, match):
    label = _project_label(match.group("id"))
    return ActivityLog.Action.SHARE_PROJECT, f"Shared project {label} via email"


@register(r"^/projects/(?P<id>\d+)/$", {"POST"})
def _project_detail_post(request, response, match):
    label = _project_label(match.group("id"))
    post = getattr(request, "POST", {})

    if "file_upload" in post:
        return ActivityLog.Action.UPLOAD_FILE, f"Uploaded a file to project {label}"
    if "add_comment" in post:
        return ActivityLog.Action.POST_COMMENT, f"Commented on project {label}"
    if "invite_member" in post:
        return (
            ActivityLog.Action.MANAGE_INVITE,
            f"Invited a collaborator to project {label}",
        )

    return ActivityLog.Action.UPDATE_PROJECT, f"Updated project {label}"


@register(r"^/projects/(?P<id>\d+)/remove-member/\d+/$", {"POST"})
def _remove_member(request, response, match):
    label = _project_label(match.group("id"))
    return (
        ActivityLog.Action.MANAGE_INVITE,
        f"Removed a collaborator from project {label}",
    )


@register(r"^/projects/(?P<id>\d+)/invite/\d+/cancel/$", {"POST"})
def _cancel_invite(request, response, match):
    label = _project_label(match.group("id"))
    return ActivityLog.Action.MANAGE_INVITE, f"Cancelled an invite for project {label}"


@register(r"^/projects/invite/[^/]+/$", {"POST"})
def _invite_response(request, response, match):
    post = getattr(request, "POST", {})

    if "accept" in post:
        return ActivityLog.Action.MANAGE_INVITE, "Accepted a project invite"
    if "decline" in post:
        return ActivityLog.Action.MANAGE_INVITE, "Declined a project invite"

    return ActivityLog.Action.MANAGE_INVITE, "Responded to a project invite"


@register(r"^/users/profile/edit/$", {"POST"})
def _edit_profile(request, response, match):
    return ActivityLog.Action.EDIT_PROFILE, "Updated your profile"


@register(r"^/users/profile/(?P<username>[^/]+)/toggle-follow/$", {"POST"})
def _toggle_follow(request, response, match):
    followed = _response_json(response).get("following")
    username = match.group("username")
    if followed is False:
        return ActivityLog.Action.FOLLOW_USER, f"Unfollowed {username}"
    return ActivityLog.Action.FOLLOW_USER, f"Followed {username}"


@register(r"^/feedback/create/$", {"POST"})
def _send_feedback(request, response, match):
    return ActivityLog.Action.SEND_FEEDBACK, "Submitted feedback"


@register(r"^/feedback/(?P<id>\d+)/delete/$", {"POST"})
def _delete_feedback(request, response, match):
    return ActivityLog.Action.OTHER, "Deleted a feedback entry"


def classify_request(request, response):
    """
    Turns a raw (method, path) into a friendlier (action, description)
    pair by matching it against known URL patterns. Falls back to a
    still-somewhat-readable generic description if nothing matches.
    """
    path = request.path
    method = request.method

    for compiled, methods, handler in _PATTERNS:
        if methods and method not in methods:
            continue

        match = compiled.match(path)
        if not match:
            continue

        result = handler(request, response, match)
        if result is not None:
            return result

    return ActivityLog.Action.OTHER, _generic_description(request)


@register(r"^/accounts/(?P<provider>[^/]+)/login/$", {"POST"})
def _social_login_start(request, response, match):
    provider = match.group("provider").capitalize()
    return ActivityLog.Action.LOGIN, f"Signed in with {provider}"
