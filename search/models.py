from django.conf import settings
from django.db import models


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_history",
    )

    query = models.CharField(max_length=200)

    searched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-searched_at"]
