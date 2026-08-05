from functools import partial

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
    feedback = form.save(commit=False)
    feedback.user = request.user

    feedback.status = Feedback.STATUS_OPEN
    feedback.save()

    request._activity_logged = True

    transaction.on_commit(
        partial(
            log_activity,
            request=request,
            user=request.user,
            action=ActivityLog.Action.SEND_FEEDBACK,
            description=f"Feedback #{feedback.pk} was submitted.",
            status_code=201,
        ),
        robust=True,
    )

    return feedback
