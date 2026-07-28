import json

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
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
from django.db.models import Count, Prefetch

def get_dashboard_data(user,projects):
    total_projects = projects.count()
    now = timezone.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    projects_this_month = projects.filter(
       created_at__gte=first_day_of_month
    ).count()
    

    today = timezone.localdate()
    week_start = today - timedelta(days=6)
    week_end = today

    weekly_activity = get_weekly_activity(user)
   
    banner_stats = [
        {
            "label": "Total Projects",
            "value": total_projects,
            "delta": f"+{projects_this_month} this month"
        },
        {
            "label": "Total Downloads",
            "value": 45,
            "delta": "+12% ↑"  
        },
        {
            "label": "Profile Views",
            "value": 55,
            "delta": "+8% ↑"  
        },
        {
            "label": "Followers",
            "value": 21,
            "delta": "+47 this week"  
        },

        
    ]



    quick_actions = [
    {
        "label": "New Project",
        "desc": "Upload your work",
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-plus-icon lucide-plus"><path d="M5 12h14"/><path d="M12 5v14"/></svg>',
        "color": "#4F46E5",
        "bg": "bg-indigo-50",
        "text_color": "text-indigo-600",
        "border_color": "border-indigo-200",
        "page": "/projects/create-project/",
    },
    {
        "label": "Upload Files",
        "desc": "Add to existing",
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-upload-icon lucide-upload"><path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/></svg>',
        "color": "#7C3AED",
        "bg": "bg-purple-50",
        "text_color": "text-purple-600",
        "border_color": "border-purple-200",
        "page": "/files/",
    },
    {
        "label": "Analytics",
        "desc": "View insights",
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-no-axes-column-icon lucide-chart-no-axes-column"><path d="M5 21v-6"/><path d="M12 21V3"/><path d="M19 21V9"/></svg>',
        "color": "#22C55E",
        "bg": "bg-green-50",
        "text_color": "text-green-600",
        "border_color": "border-green-200",
        "page": "/analytics/",
    },
    {
        "label": "Notifications",
        "desc": "3 unread",
        "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bell-icon lucide-bell"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
        "color": "#F59E0B",
        "bg": "bg-amber-50",
        "text_color": "text-amber-500",
        "border_color": "border-amber-200",
        "page": "/notifications/",
    },
     ]
    

    return { 'banner_stats': get_banner_stats(user) ,    
            "stats": get_stats(user),
            "weekly_activity": get_weekly_activity(user),
            "project_perf": get_project_perf(projects),
            "recent_activity": get_recent_activity(user),
            "quick_actions": quick_actions,
            "storage_pie": get_project_storage(projects,user),
            "recent_projects": get_recent_projects(projects),
            "page_title": "Dashboard",
            "explore_projects": get_explore_projects(user),
            "week_start": week_start,
            "week_end": week_end,


            }
    
    

def format_bytes(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

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
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-folder-open-icon lucide-folder-open"><path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/></svg>',
            "icon_bg": "bg-indigo-100",
            "icon_color": "text-indigo-600",
            "sub_color": "text-indigo-600",
        },
        {
            "label": "Uploads",
            "value": files.count(),
            "sub": "Total uploaded files",
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-upload-icon lucide-upload"><path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/></svg>',
            "icon_bg": "bg-purple-100",
            "icon_color": "text-purple-600",
            "sub_color": "text-purple-600",
        },
        {
            "label": "Storage",
            "value": format_bytes(sum(f.file.size for f in files)),
            "sub": "Bytes used",
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-download-icon lucide-download"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></svg>',
            "icon_bg": "bg-green-50",
            "icon_color": "text-green-500",
            "sub_color": "text-green-500",
        },
        {
            "label": "Followers",
            "value": user.followers.count(),
            "sub": "People following you",
            "icon": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users-round-icon lucide-users-round"><path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3.37-2-6.5-4-8a5 5 0 0 0-.45-8.3"/></svg>',
            "icon_bg": "bg-amber-50",
            "icon_color": "text-amber-500",
            "sub_color": "text-amber-500",
        },
    ]
    
 

def get_banner_stats(user):
    projects = Project.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()

    now = timezone.now()
    month_ago = now - timedelta(days=30)
    week_ago = now - timedelta(days=7)

    total_projects = projects.count()

    projects_this_month = projects.filter(
        created_at__gte=month_ago
    ).count()

    total_downloads = projects.aggregate(
        total=Sum("download_count")
    )["total"] or 0

    downloads_this_month = projects.filter(
        created_at__gte=month_ago
    ).aggregate(
        total=Sum("download_count")
    )["total"] or 0

    total_views = projects.aggregate(
        total=Sum("views_count")
    )["total"] or 0

    followers = user.followers.count()

    return [
        {
            "label": "Total Projects",
            "value": total_projects,
            "delta": f"+{projects_this_month} this month"
        },
        {
            "label": "Total Downloads",
            "value": total_downloads,
            "delta": f"+{downloads_this_month} this month"
        },
        {
            "label": "Profile Views",
            "value": total_views,
            "delta": "Total project views"
        },
        {
            "label": "Followers",
            "value": followers,
            "delta": "Your community"
        },
    ]
    
def get_project_perf(projects):

    return [
        {
            "name": p.title,
            "downloads": p.download_count,
            "likes": p.like_count
        }
        for p in projects[:5]
    ]
    
def get_project_storage(projects, user):
    image_exts = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'}
    pdf_exts = {'pdf'}
    doc_exts = {
        'doc', 'docx',
        'xls', 'xlsx',
        'ppt', 'pptx',
        'odt', 'ods', 'odp',
        'rtf', 'txt'
    }

    files = ProjectFile.objects.filter(
        project__in=projects,
        uploaded_by=user
    )

    images = 0
    PDFs = 0
    docs = 0
    other = 0

    for f in files:
        ext = f.file.name.rsplit('.', 1)[-1].lower()

        if ext in image_exts:
            images += 1
        elif ext in pdf_exts:
            PDFs += 1
        elif ext in doc_exts:
            docs += 1
        else:
            other += 1

    return {
        "images": images,
        "PDFs": PDFs,
        "docs": docs,
        "other": other,
    }    
      
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

    projects = Project.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()

    data = []

    for i in range(7):
        day = start_date + timedelta(days=i)

        uploads = ProjectFile.objects.filter(
            uploaded_by=user,
            uploaded_at__date=day
        ).count()


        downloads = projects.filter(
            created_at__date=day
        ).aggregate(
            total=Sum("download_count")
        )["total"] or 0


        views = projects.filter(
            created_at__date=day
        ).aggregate(
            total=Sum("views_count")
        )["total"] or 0


        data.append({
            "day": day.strftime("%a"),
            "uploads": uploads,
            "downloads": downloads,
            "views": views,
        })


    return data



def get_explore_projects(user, limit=4):
    """Public projects from other users, sorted by most likes first."""
    return (
        Project.objects
        .filter(visibility=Project.PUBLIC)
        .exclude(owner=user)
        .exclude(memberships__user=user)
        .select_related("owner")
        .prefetch_related(
            Prefetch(
                "files",
                queryset=ProjectFile.objects.order_by("uploaded_at"),
                to_attr="preview_files"
            )
        )
        .annotate(likes_count=Count("likes"))  
        .order_by("-likes_count", "-created_at")
        [:limit]
    )