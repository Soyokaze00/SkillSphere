from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import ActivityLog
from .services import log_activity


@receiver(user_logged_in)
def record_user_login(sender, request, user, **kwargs):
    if request is None:
        return

    log_activity(
        request=request,
        user=user,
        action=ActivityLog.Action.LOGIN,
        description="User logged in successfully.",
        status_code=200,
    )


@receiver(user_logged_out)
def record_user_logout(sender, request, user, **kwargs):
    if request is None or user is None:
        return

    log_activity(
        request=request,
        user=user,
        action=ActivityLog.Action.LOGOUT,
        description="User logged out successfully.",
        status_code=200,
    )