from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import ActivityLog


@login_required
def activity_list(request):
    logs_queryset = (
        ActivityLog.objects
        .filter(user=request.user)
        .select_related("user")
        .order_by("-created_at")
    )

    paginator = Paginator(logs_queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "activity_logs/activity_list.html",
        {
            "page_obj": page_obj,
            "logs": page_obj.object_list,
        },
    )