from django.urls import path

from . import views


app_name = "feedback"

urlpatterns = [
    path(
        "",
        views.feedback_index,
        name="feedback",
    ),
    path(
        "create/",
        views.feedback_create,
        name="create",
    ),
    path(
        "mine/",
        views.my_feedback_list,
        name="my-feedback-list",
    ),
    path(
        "<int:feedback_id>/",
        views.feedback_detail,
        name="detail",
    ),
    path(
        "<int:feedback_id>/delete/",
        views.feedback_delete,
        name="delete",
    ),
]
