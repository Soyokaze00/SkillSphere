# search/views.py
from django.shortcuts import render
from django.db.models import Q
from projects.models import Project
from search.models import SearchHistory
from django.shortcuts import redirect
from django.http import JsonResponse
from projects.models import Project
from users.models import CustomUser
from django.db.models import Q
from django.core.paginator import Paginator

def search_view(request):
    status = request.GET.get("status", "")
    projects = Project.objects.none()   
    query = request.GET.get("q", "").strip()
    users = CustomUser.objects.none()
    search_type = request.GET.get("type", "all")
   
    if query:
     users = CustomUser.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    )
    if query:
     SearchHistory.objects.update_or_create(
        user=request.user,
        query=query
    )
     
    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(owner__username__icontains=query),
            visibility=Project.PUBLIC
    )
        
    if status:
        projects = projects.filter(status=status)

    recent_searches = SearchHistory.objects.filter(
      user=request.user
    )[:5]
    
    
    suggested_searches = (
    Project.objects
    .filter(visibility="PUBLIC")
    .order_by("-created_at")[:5]
     )
    
    if search_type == "projects":
       users = CustomUser.objects.none()

    elif search_type == "users":
        projects = Project.objects.none()

    projects_count = projects.count()
    users_count = users.count()
    total_count = projects_count + users_count
    
    paginator = Paginator(projects, 10)
    page = request.GET.get("page")
    projects = paginator.get_page(page)
        
    context = {
        'query': query,
        'projects': projects,
        "status": status,
        "recent_searches": recent_searches,
        "suggested_searches":suggested_searches,
        "users": users,
        "projects_count": projects_count,
        "users_count": users_count,
        "page_title": "Search",
        "total_count":total_count
        


    }    
    return render(request, 'search/search.html', context)




def clear_search_history(request):

    SearchHistory.objects.filter(
        user=request.user
    ).delete()

    return redirect("search:search")


def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({"projects": [], "users": []})

    projects = (
        Project.objects
        .filter(
            visibility="PUBLIC",
            title__icontains=query
        )[:5]
    )

    users = (
        CustomUser.objects
        .filter(username__icontains=query)[:5]
    )

    return JsonResponse({
        "projects":[
            {
                "id":p.id,
                "title":p.title
            }
            for p in projects
        ],

        "users":[
            {
                "id":u.id,
                "username":u.username
            }
            for u in users
        ]
    })
    
    
