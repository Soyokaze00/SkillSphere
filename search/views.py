
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Case, When
from django.core.paginator import Paginator
from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity

from projects.models import Project
from projects.documents import ProjectDocument
from users.models import CustomUser
from search.models import SearchHistory


def search_projects(query):

    s = (
        ProjectDocument.search()
        .query(
            "multi_match",
            query=query,
            fields=[
                "title^3",
                "tags^2",
                "description",
            ],
            fuzziness="AUTO",
        )
        .highlight(
            "title",
            "description",
            "tags",
            pre_tags=["<mark>"],
            post_tags=["</mark>"],
        )
    )

    response = s.execute()

    ids = [int(hit.meta.id) for hit in response]

    if not ids:
        return Project.objects.none()

    projects = {
        p.id: p
        for p in Project.objects.filter(pk__in=ids)
        .select_related("owner")
    }

    result = []

    for hit in response:
        project = projects[int(hit.meta.id)]

        if hasattr(hit.meta, "highlight"):

           project.highlight_title = (
              hit.meta.highlight.title[0]
              if "title" in hit.meta.highlight
              else project.title
        )  

           project.highlight_description = (
              hit.meta.highlight.description[0]
              if "description" in hit.meta.highlight
              else project.description
        )

           project.highlight_tags = (
             hit.meta.highlight.tags
             if "tags" in hit.meta.highlight
             else project.tag_list
         ) 

        else:
          project.highlight_title = project.title
          project.highlight_description = project.description
          project.highlight_tags = project.tag_list

        result.append(project)

    return result



def search_users(query):
    from users.documents import UserDocument

    s = UserDocument.search().query(
    "bool",
    should=[
        {
            "multi_match": {
                "query": query,
                "fields": [
                    "username^3",
                    "first_name",
                    "last_name",
                ],
                "fuzziness": "AUTO",
            }
        },
        {
            "prefix": {
                "username.keyword": query.lower()
            }
        }
    ],
    minimum_should_match=1,
    )

    response = s.execute()
    ids = [int(hit.meta.id) for hit in response]

    if not ids:
        return CustomUser.objects.none()

    preserved_order = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(ids)]
    )
    return CustomUser.objects.filter(pk__in=ids).order_by(preserved_order)



def search_view(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    search_type = request.GET.get("type", "all")
    page = request.GET.get("page", 1)

    projects = Project.objects.none()
    users = CustomUser.objects.none()
    all_projects = Project.objects.none()
    all_users = CustomUser.objects.none()

    if query:
        if request.user.is_authenticated:
            SearchHistory.objects.update_or_create(
                user=request.user,
                query=query,
                defaults={"query": query},
            )

        all_projects = search_projects(query)
        all_users = search_users(query)

        if status:
            all_projects = all_projects.filter(status=status)

        projects_count = len(all_projects)
        users_count = len(all_users)

        if search_type == "projects":
            projects = all_projects
        elif search_type == "users":
            users = all_users
        else:
            projects = all_projects
            users = all_users
    else:
        projects_count = 0
        users_count = 0

    recent_searches = (
        SearchHistory.objects.filter(user=request.user)[:5]
        if request.user.is_authenticated else []
    )

    projects_page = projects
    users_page = users

    if search_type != "users":
        paginator = Paginator(projects, 10)
        projects_page = paginator.get_page(page)

    if search_type != "projects":
        paginator = Paginator(users, 10)
        users_page = paginator.get_page(page)

    exclude_ids = []
    if search_type != "users":
        exclude_ids = [p.id for p in projects_page]
        
    if query:
      suggested_searches = get_project_suggestions_es(query)
    else:
      suggested_searches = get_initial_suggestions()

    context = {
        'query': query,
        'projects': projects_page,
        'status': status,
        'search_type': search_type,
        'current_status': status,
        'current_type': search_type,
        "users": users_page,
        'recent_searches': recent_searches,
        "suggested_searches": suggested_searches,
        'projects_count': projects_count,
        'users_count': users_count,
        'total_count': projects_count + users_count,
        'page_title': "Search",
    }
    return render(request, 'search/search.html', context)




@login_required
@require_POST
def clear_search_history(request):
    SearchHistory.objects.filter(user=request.user).delete()
    return redirect("search:search")



def get_initial_suggestions(limit=5):
    search = (
        ProjectDocument.search()
        .extra(size=limit)
    )

    response = search.execute()

    return [
        {
            "id": hit.meta.id,
            "title": hit.title,
        }
        for hit in response
    ]
    
def get_project_suggestions_es(query, limit=5):
    if not query:
        return []

    search = (
        ProjectDocument.search()
        .query(
            "bool",
            should=[
                {
                    "match_phrase_prefix": {
                        "title": query
                    }
                },
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^3",
                            "tags^2",
                            "description"
                        ],
                        "fuzziness": "AUTO"
                    }
                }
            ],
            minimum_should_match=1
        )
        .extra(size=limit)
    )

    response = search.execute()

    return [
        {
            "id": hit.meta.id,
            "title": hit.title,
        }
        for hit in response
    ]
    
    
def get_user_suggestions_es(query, limit=5):
    if not query:
        return []

    from users.documents import UserDocument

    search = (
        UserDocument.search()
        .query(
            "multi_match",
            query=query,
            fields=[
                "username^2",
                "first_name",
                "last_name",
            ],
            fuzziness="AUTO",
        )
        .extra(size=limit)
    )

    response = search.execute()

    return [
        {
            "id": hit.meta.id,
            "username": hit.username,
        }
        for hit in response
    ]
   
   
    
def search_suggestions(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return JsonResponse({
            "projects": [],
            "users": []
        })


    projects = get_project_suggestions_es(query)

    users = get_user_suggestions_es(query)


    return JsonResponse({
        "projects": projects,
        "users": users,
    })