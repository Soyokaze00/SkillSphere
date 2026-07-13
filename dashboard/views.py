# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# @login_required
# def home(request):
#     return render(request, "dashboard/home.html")

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
def home(request):
    start = time.perf_counter()

    projects = Project.objects.filter(
        Q(owner=request.user)
        |
        Q(memberships__user=request.user)
    ).distinct()


    print("Dashboard:", time.perf_counter() - start)


    return render(request, "dashboard/home.html", get_dashboard_data(request.user , projects))

    
    

