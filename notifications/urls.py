from django.urls import path
from . import views
app_name = "notifications"

urlpatterns = [

    path(
        "",
        views.notification_center,
        name="notification_center"
    ),
    path("read/<int:pk>/", views.mark_as_read, name="mark-as-read"),
    path("delete/<int:pk>/", views.delete_notification, name="delete"),
    path("mark-all-read/", views.mark_all_as_read, name="mark_all_as_read"),
    path("delete-all/", views.delete_all_notifications, name="delete_all"),
]