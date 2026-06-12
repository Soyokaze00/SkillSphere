from django.urls import path
from .views import (
    create_project,
    project_list,
    project_detail
)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project-list"),
    path("create-project/", create_project, name="create-project"),
    path("<int:project_id>/", project_detail, name='project-detail')
]