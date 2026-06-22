from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from notifications.utils import get_notification_style
from projects.models import Project
from projects.models import Project, ProjectFile
from django.db.models import Q
from notifications.models import Notification
from django.utils import timezone
from datetime import timedelta

def get_dashboard_data(user,projects):


    total_projects = projects.count()
    
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    projects_this_month = projects.filter(
       created_at__gte=first_day_of_month
    ).count()
    

    
    banner_stats = [
        {
            "label": "Total Projects",
            "value": total_projects,
            "delta": f"+{projects_this_month} this month"
        },
        {
            "label": "Total Downloads",
            "value": 45,
            "delta": "+12% ↑"  # فعلاً همین بمونه
        },
        {
            "label": "Profile Views",
            "value": 55,
            "delta": "+8% ↑"  # فعلاً همین بمونه
        },
        {
            "label": "Followers",
            "value": 21,
            "delta": "+47 this week"  # فعلاً همین بمونه
        },

        
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

    return { 'banner_stats': banner_stats ,    
            "stats": get_stats(user),
            "weekly_activity": get_weekly_activity(user),
            "project_perf": get_project_perf(projects),
            "recent_activity": get_recent_activity(user),
            "quick_actions": quick_actions,
            "recent_projects": get_recent_projects(projects),}
    
    


def get_stats(user):

    projects = Project.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()

    files = ProjectFile.objects.filter(project__in=projects)

    return [
        {
            "label": "Projects",
            "value": projects.count(),
            "sub": "All your projects",
            "icon": "folder-open",
            "icon_bg": "bg-indigo-100",
            "icon_color": "text-indigo-600",
            "sub_color": "text-indigo-600",
        },
        {
            "label": "Uploads",
            "value": files.count(),
            "sub": "Total uploaded files",
            "icon": "upload",
            "icon_bg": "bg-purple-100",
            "icon_color": "text-purple-600",
            "sub_color": "text-purple-600",
        },
        {
            "label": "Storage",
            "value": sum(f.file.size for f in files),
            "sub": "Bytes used",
            "icon": "download",
            "icon_bg": "bg-green-50",
            "icon_color": "text-green-500",
            "sub_color": "text-green-500",
        },
        {
            "label": "Followers",
            "value": 0,
            "sub": "Coming soon",
            "icon": "users",
            "icon_bg": "bg-amber-50",
            "icon_color": "text-amber-500",
            "sub_color": "text-amber-500",
        },
    ]
    
    

def get_project_perf(projects):

    return [
        {
            "name": p.title,
            "downloads": p.files.count(),
            "stars": 0 
        }
        for p in projects[:5]
    ]
    

def get_recent_activity(user):
    
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
    
    notifications=Notification.objects.filter(user=user).order_by('-id')[:5]

    for n in notifications:
        n.style = get_notification_style(n.type)

    
    return notifications 



def get_recent_projects(projects):
    return projects.order_by('-created_at')[:4]


def get_weekly_activity(user):

    today = timezone.now().date()
    start_date = today - timedelta(days=6)

    files = ProjectFile.objects.filter(
        uploaded_by=user,
        uploaded_at__date__gte=start_date
    )

    data = []

    for i in range(7):
        day = start_date + timedelta(days=i)

        count = files.filter(uploaded_at__date=day).count()

        data.append({
            "day": day.strftime("%a"),
            "uploads": count,
            "downloads": 0,
            "views": 0
        })

    return data