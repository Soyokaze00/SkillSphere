from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from .forms import FeedbackForm
from .models import Feedback
from .services import create_feedback


@login_required
def feedback_center(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)

        if form.is_valid():
            create_feedback(
                request=request,
                form=form,
            )

            messages.success(
                request,
                "Your feedback was submitted successfully.",
            )
            return redirect("feedback")
    else:
        form = FeedbackForm(
            initial={
                "type": Feedback.TYPE_SUGGESTION,
                "rating": 0,
            }
        )

    user_feedbacks = Feedback.objects.filter(user=request.user).order_by("-created_at")

    stats = user_feedbacks.aggregate(
        submitted=Count("pk"),
        resolved=Count(
            "pk",
            filter=Q(status=Feedback.STATUS_RESOLVED),
        ),
        in_review=Count(
            "pk",
            filter=Q(status=Feedback.STATUS_IN_REVIEW),
        ),
        planned=Count(
            "pk",
            filter=Q(status=Feedback.STATUS_PLANNED),
        ),
    )

    paginator = Paginator(user_feedbacks, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    form_state = {
        "type": (form["type"].value() or Feedback.TYPE_SUGGESTION),
        "rating": form["rating"].value() or 0,
        "subject": form["subject"].value() or "",
        "message": form["message"].value() or "",
    }

    context = {
        "form": form,
        "form_state": form_state,
        "prev_feedback": page_obj,
        "page_obj": page_obj,
        "stats": stats,
    }

    return render(
        request,
        "feedback/feedback.html",
        context,
    )
