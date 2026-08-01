# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# @login_required
# def home(request):
#     return render(request, "dashboard/home.html")

from projects.recommendation_service import (
    recommend_projects_for_user,
)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
import time

from dashboard.services import get_dashboard_data
from projects.models import Project
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime

@login_required
@login_required
def home(request):
    start = time.perf_counter()

    projects = Project.objects.filter(
        Q(owner=request.user)
        | Q(memberships__user=request.user)
    ).distinct()

    context = get_dashboard_data(
        request.user,
        projects,
    )

    try:
        context["recommended_projects"] = (
            recommend_projects_for_user(
                request.user,
                limit=4,
            )
        )
    except Exception as error:
        print("Recommendation error:", error)
        context["recommended_projects"] = []

    print(
        "Dashboard:",
        time.perf_counter() - start,
    )

    return render(
        request,
        "dashboard/home.html",
        context,
    )
    
    


