from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import FeedbackForm
from .models import Feedback


@login_required
def feedback_center(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Your feedback was submitted successfully.")
            return redirect("feedback")
    else:
        form = FeedbackForm(initial={"type": "suggestion", "rating": 0})

    user_feedbacks = Feedback.objects.filter(user=request.user)

    stats = {
        "submitted": user_feedbacks.count(),
        "resolved": user_feedbacks.filter(status=Feedback.STATUS_RESOLVED).count(),
        "in_review": user_feedbacks.filter(status=Feedback.STATUS_IN_REVIEW).count(),
        "planned": user_feedbacks.filter(status=Feedback.STATUS_PLANNED).count(),
    }

    context = {
        "form": form,
        "prev_feedback": user_feedbacks[:10],
        "stats": stats,
    }
    return render(request, "feedback/feedback.html", context)