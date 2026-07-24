from .models import ActivityLog
from .services import log_activity


class ActivityLogMiddleware:
    """
    Log successful state-changing requests made by authenticated users.
    """

    TRACKED_METHODS = {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }

    IGNORED_PATH_PREFIXES = (
        "/static/",
        "/media/",
        "/admin/jsi18n/",
        "/admin/login/",
        "/admin/logout/",
        "/accounts/login/",
        "/accounts/logout/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self.should_log(request, response):
            log_activity(
                request=request,
                action=ActivityLog.Action.OTHER,
                description=(
                    f"{request.method} request to {request.path}"
                ),
                status_code=response.status_code,
            )

        return response

    def should_log(self, request, response):
        user = getattr(request, "user", None)

        if user is None or not user.is_authenticated:
            return False

        if request.method not in self.TRACKED_METHODS:
            return False

        if not 200 <= response.status_code < 400:
            return False

        if request.path.startswith(self.IGNORED_PATH_PREFIXES):
            return False

        return True