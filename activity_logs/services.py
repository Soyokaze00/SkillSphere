from django.http import HttpRequest

from .models import ActivityLog


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