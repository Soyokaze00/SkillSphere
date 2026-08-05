from django.urls import path

from .views import (
    cancel_invite,
    create_project,
    delete_project,
    download_all_files,
    edit_project,
    file_detail,
    invite_landing,
    project_detail,
    project_list,
    remove_member,
    share_project_email,
    toggle_like,
)

app_name = "projects"

urlpatterns = [
    path("", project_list, name="project-list"),
    path("create-project/", create_project, name="create-project"),
    path("<int:project_id>/", project_detail, name="project-detail"),
    path("<int:project_id>/like/", toggle_like, name="toggle-like"),
    path("<int:project_id>/download-all/", download_all_files, name="download-all"),
    path("file/<int:file_id>/", file_detail, name="file-detail"),
    path("<int:project_id>/edit/", edit_project, name="project-edit"),
    path("<int:project_id>/delete/", delete_project, name="delete-project"),
    path("<int:project_id>/share-email/", share_project_email, name="share-email"),
    path(
        "<int:project_id>/remove-member/<int:user_id>/",
        remove_member,
        name="remove-member",
    ),
    path(
        "<int:project_id>/invite/<int:invitation_id>/cancel/",
        cancel_invite,
        name="cancel-invite",
    ),
    path("invite/<str:token>/", invite_landing, name="invite-landing"),
]
