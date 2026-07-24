from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from .forms import FeedbackForm
from .models import Feedback
from .services import create_feedback


def serialize_feedback(feedback):
    return {
        "id": feedback.id,
        "subject": feedback.subject,
        "category": feedback.category,
        "category_display": feedback.get_category_display(),
        "message": feedback.message,
        "status": feedback.status,
        "status_display": feedback.get_status_display(),
        "admin_response": feedback.admin_response,
        "created_at": feedback.created_at.isoformat(),
        "updated_at": feedback.updated_at.isoformat(),
    }


@login_required
@require_POST
def feedback_create(request):
    """
    Create feedback for the currently authenticated user.
    """
    form = FeedbackForm(request.POST)

    if not form.is_valid():
        return JsonResponse(
            {
                "success": False,
                "errors": form.errors.get_json_data(),
            },
            status=400,
        )

    feedback = create_feedback(
        request=request,
        form=form,
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Feedback submitted successfully.",
            "feedback": serialize_feedback(feedback),
        },
        status=201,
    )


@login_required
@require_GET
def my_feedback_list(request):
    """
    Return only the current user's feedbacks.
    """
    feedbacks = Feedback.objects.filter(
        user=request.user
    )

    return JsonResponse(
        {
            "success": True,
            "count": feedbacks.count(),
            "feedbacks": [
                serialize_feedback(feedback)
                for feedback in feedbacks
            ],
        }
    )


@login_required
@require_GET
def feedback_detail(request, feedback_id):
    """
    Return one feedback belonging to the current user.
    """
    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        user=request.user,
    )

    return JsonResponse(
        {
            "success": True,
            "feedback": serialize_feedback(feedback),
        }
    )


@login_required
@require_POST
def feedback_delete(request, feedback_id):
    """
    Delete one feedback belonging to the current user.
    """
    feedback = get_object_or_404(
        Feedback,
        id=feedback_id,
        user=request.user,
    )

    feedback.delete()

    return JsonResponse(
        {
            "success": True,
            "message": "Feedback deleted successfully.",
        }
    )
def feedback_index(request):
    return JsonResponse(
        {
            "success": True,
            "message": "Feedback backend is running.",
            "endpoints": {
                "create": {
                    "method": "POST",
                    "url": "/feedback/create/",
                },
                "my_feedbacks": {
                    "method": "GET",
                    "url": "/feedback/mine/",
                },
                "detail": {
                    "method": "GET",
                    "url": "/feedback/<id>/",
                },
                "delete": {
                    "method": "POST",
                    "url": "/feedback/<id>/delete/",
                },
            },
        }
    )