# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required


# @login_required
# def home(request):
#     return render(request, "dashboard/home.html")

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json

@login_required
def home(request):

    banner_stats = [
        {"label": "Total Projects", "value": "24", "delta": "+3 this month"},
        {"label": "Total Downloads", "value": "8,432", "delta": "+12% ↑"},
        {"label": "Profile Views", "value": "14,721", "delta": "+8% ↑"},
        {"label": "Followers", "value": "1,284", "delta": "+47 this week"},
    ]

    stats = [
        {
            "label": "Projects",
            "value": 24,
            "sub": "3 this month",
            "icon": "folder-open",
            "icon_bg": "bg-indigo-100",
            "icon_color": "text-indigo-600",
            "sub_color": "text-indigo-600"
        },
        {
            "label": "Uploads",
            "value": 147,
            "sub": "12 this week",
            "icon": "upload",
            "icon_bg": "bg-purple-100",
            "icon_color": "text-purple-600",
            "sub_color": "text-purple-600"
        },
        {
            "label": "Downloads",
            "value": "8,432",
            "sub": "+12% this month",
            "icon": "download",
            "icon_bg": "bg-green-50",
            "icon_color": "text-green-500",
            "sub_color": "text-green-500"
        },
        {
            "label": "Followers",
            "value": "1,284",
            "sub": "+47 this week",
            "icon": "users",
            "icon_bg": "bg-amber-50",
            "icon_color": "text-amber-500",
            "sub_color": "text-amber-500"
        },
    ]

    # charts
    weekly_activity = [
        {"day": "Mon", "downloads": 18, "views": 45, "uploads": 3},
        {"day": "Tue", "downloads": 24, "views": 62, "uploads": 5},
        {"day": "Wed", "downloads": 31, "views": 58, "uploads": 2},
        {"day": "Thu", "downloads": 42, "views": 87, "uploads": 8},
        {"day": "Fri", "downloads": 38, "views": 94, "uploads": 6},
        {"day": "Sat", "downloads": 29, "views": 71, "uploads": 4},
        {"day": "Sun", "downloads": 35, "views": 83, "uploads": 7},
    ]
    
    project_perf = [
    {"name": "Brand Kit", "downloads": 412, "stars": 88},
    {"name": "UI Lib", "downloads": 387, "stars": 142},
    {"name": "Dashboard", "downloads": 298, "stars": 76},
    {"name": "Icon Pack", "downloads": 521, "stars": 193},
    {"name": "Font Set", "downloads": 164, "stars": 41},
    ]

    recent_activity = [
        {
            "icon": "download",
            "text": "Sarah Chen downloaded your Brand Identity Kit",
            "time": "2m ago",
            "color": "#4F46E5",
            "bg": "bg-indigo-50",
            "text_color": "text-indigo-600",
        },
        {
            "icon": "star",
            "text": "Marcus Rivera starred Mobile App UI Kit",
            "time": "18m ago",
            "color": "#F59E0B",
            "bg": "bg-amber-50",
            "text_color": "text-amber-500",
        },
        {
            "icon": "eye",
            "text": "Your Analytics Dashboard reached 1,500 views",
            "time": "1h ago",
            "color": "#7C3AED",
            "bg": "bg-purple-50",
            "text_color": "text-purple-600",
        },
        {
            "icon": "users",
            "text": "Daniel Kim started following you",
            "time": "3h ago",
            "color": "#22C55E",
            "bg": "bg-green-50",
            "text_color": "text-green-600",
        },
        {
            "icon": "download",
            "text": "Icon Pack reached 500 downloads",
            "time": "5h ago",
            "color": "#4F46E5",
            "bg": "bg-indigo-50",
            "text_color": "text-indigo-600",
        },
    ]

    quick_actions = [
    {
        "label": "New Project",
        "desc": "Upload your work",
        "icon": "plus",
        "color": "#4F46E5",
        "bg": "bg-indigo-50",
        "text_color": "text-indigo-600",
        "border_color": "border-indigo-200",
        "page": "/create-project/",
    },
    {
        "label": "Upload Files",
        "desc": "Add to existing",
        "icon": "upload",
        "color": "#7C3AED",
        "bg": "bg-purple-50",
        "text_color": "text-purple-600",
        "border_color": "border-purple-200",
        "page": "/files/",
    },
    {
        "label": "Analytics",
        "desc": "View insights",
        "icon": "bar-chart-2",
        "color": "#22C55E",
        "bg": "bg-green-50",
        "text_color": "text-green-600",
        "border_color": "border-green-200",
        "page": "/analytics/",
    },
    {
        "label": "Notifications",
        "desc": "3 unread",
        "icon": "bell",
        "color": "#F59E0B",
        "bg": "bg-amber-50",
        "text_color": "text-amber-500",
        "border_color": "border-amber-200",
        "page": "/notifications/",
    },
     ]
    
    recent_projects = [
    {
        "id": 1,
        "title": "Brand Identity Kit",
        "image": "https://images.unsplash.com/photo-1561070791-2526d30994b5?w=400",
        "status": "published",
        "downloads": 412,
        "stars": 88,
        "updated_at": "2h ago",
    },
    {
        "id": 2,
        "title": "Mobile App UI Kit",
        "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400",
        "status": "published",
        "downloads": 387,
        "stars": 142,
        "updated_at": "1d ago",
    },
    {
        "id": 3,
        "title": "Analytics Dashboard",
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400",
        "status": "published",
        "downloads": 298,
        "stars": 76,
        "updated_at": "3d ago",
    },
    {
        "id": 4,
        "title": "E-commerce Illustrations",
        "image": "https://images.unsplash.com/photo-1472851294608-062f824d29cc?w=400",
        "status": "draft",
        "downloads": 521,
        "stars": 193,
        "updated_at": "5d ago",
    },
    ]
    context = {
    "banner_stats": banner_stats,
    "stats": stats,
    "weekly_activity": weekly_activity,
    "project_perf": project_perf,
    "recent_activity": recent_activity,
    "quick_actions": quick_actions,
    "recent_projects": recent_projects,
    }

    return render(request, "dashboard/home.html", context)

    
    

