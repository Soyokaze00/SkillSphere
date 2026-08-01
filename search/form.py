from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
)
from django.db.models import F, query

from projects.models import Project

projects = (
    Project.objects.annotate(
        search=SearchVector(
            "title",
            weight="A"
        ) + SearchVector(
            "description",
            weight="B"
        )
    )
    .annotate(
        rank=SearchRank(
            F("search"),
            SearchQuery(query)
        )
    )
    .filter(rank__gte=0.1)
    .order_by("-rank")
)