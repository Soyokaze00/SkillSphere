from django.db import transaction

from activity_logs.models import ActivityLog
from activity_logs.services import log_activity

from .forms import FeedbackForm
from .models import Feedback


@transaction.atomic
def create_feedback(
    *,
    request,
    form: FeedbackForm,
) -> Feedback:
    """
    Create feedback for the authenticated user and record the activity.
    """
    feedback = form.save(commit=False)

    feedback.user = request.user
    feedback.status = Feedback.Status.PENDING

    feedback.save()

    log_activity(
        request=request,
        action=ActivityLog.Action.SEND_FEEDBACK,
        description=f"Feedback #{feedback.pk} was submitted.",
        status_code=201,
    )

    request._activity_logged = True

    return feedback