from django.urls import path

from . import views

urlpatterns = [
    path("", views.feedback_center, name="feedback"),
]