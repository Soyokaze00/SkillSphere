from dashboard.recommendation_service import recommend_projects_for_user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import time

from dashboard.services import (
    get_dashboard_data,
    get_explore_projects,
    get_followed_users_most_liked_projects,
    get_user_top_projects,
)
from projects.models import Project
from django.db.models import Q


@login_required
def home(request):
    start = time.perf_counter()

    projects = Project.objects.filter(
        Q(owner=request.user) | Q(memberships__user=request.user)
    ).distinct()

    context = get_dashboard_data(request.user, projects)

    try:
        context["recommended_projects"] = recommend_projects_for_user(request.user, limit=4)
    except Exception as error:
        print("Recommendation error:", error)
        context["recommended_projects"] = []

    print("Dashboard:", time.perf_counter() - start)

    return render(request, "dashboard/home.html", context)


@login_required
def explore_projects(request):
    user = request.user

    explore_queryset = get_explore_projects(user)
    paginator = Paginator(explore_queryset, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "dashboard/_explore_results.html", {"page_obj": page_obj})

    my_top_projects = get_user_top_projects(user, limit=4)
    followed_top_projects = get_followed_users_most_liked_projects(user, limit=4)

    context = {
        "my_top_projects": my_top_projects,
        "followed_top_projects": followed_top_projects,
        "page_obj": page_obj,
        "page_title": "Explore",
    }

    return render(request, "dashboard/explore.html", context)