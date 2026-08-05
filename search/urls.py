# search/urls.py
from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("", views.search_view, name="search"),
    # path(
    # "search/clear/",
    # views.clear_search_history,
    # name="clear_search_history"
    # ),
    path("clear/", views.clear_search_history, name="clear_search_history"),
    path("suggestions/", views.search_suggestions, name="search_suggestions"),
    # path('api/', views.search_api, name='search_api'),
]
