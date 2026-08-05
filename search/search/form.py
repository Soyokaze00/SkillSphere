from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
from django.db.models import F

from projects.models import Project


def search_projects(query):
    projects = (
        Project.objects.annotate(search=SearchVector("title", weight="A") + SearchVector("description", weight="B"))
        .annotate(
            rank=SearchRank(
                F("search"),
                SearchQuery(query),
            )
        )
        .filter(rank__gte=0.1)
        .order_by("-rank")
    )

    return projects
