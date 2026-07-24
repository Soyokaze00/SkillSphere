from django.http import HttpRequest

from .models import ActivityLog


def get_client_ip(request: HttpRequest) -> str | None:
    """
    Return the real client IP address.

    HTTP_X_FORWARDED_FOR may contain multiple IP addresses when the
    application is behind a proxy. The first value is the client IP.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def log_activity(
    *,
    request: HttpRequest,
    action: str,
    description: str = "",
    user=None,
    status_code: int | None = None,
) -> ActivityLog:
    """
    Create and return a user activity record.
    """
    activity_user = user or getattr(request, "user", None)

    if not getattr(activity_user, "is_authenticated", False):
        activity_user = None

    return ActivityLog.objects.create(
        user=activity_user,
        action=action,
        description=description,
        path=request.path,
        method=request.method,
        status_code=status_code,
        ip_address=get_client_ip(request),
    )