from django.urls import path
from .views import (
    create_project,
    explore_projects,
    project_list,
    project_detail,
    file_detail,
    toggle_like,
    download_all_files,
    edit_project,
    delete_project,
    share_project_email,
    remove_member,
    invite_landing,
    cancel_invite,
)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project-list"),
    path("create-project/", create_project, name="create-project"),
    path("<int:project_id>/", project_detail, name='project-detail'),
    path("<int:project_id>/like/", toggle_like, name='toggle-like'),
    path("<int:project_id>/download-all/", download_all_files, name='download-all'),
    path("file/<int:file_id>/", file_detail, name='file-detail'),
    path('<int:project_id>/edit/', edit_project, name='project-edit'),
    path('<int:project_id>/delete/', delete_project, name='delete-project'),
    path("<int:project_id>/share-email/", share_project_email, name='share-email'),
    path("<int:project_id>/remove-member/<int:user_id>/", remove_member, name='remove-member'),
    path("<int:project_id>/invite/<int:invitation_id>/cancel/", cancel_invite, name='cancel-invite'),
    path("invite/<str:token>/", invite_landing, name='invite-landing'),
    path("explore/", explore_projects, name="explore"), 

]