from django.urls import path

from .views import explore_projects, home

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("explore/", explore_projects, name="explore"),
]
