from django.urls import path
from .views import (
    email_verification_view,
    complete_signup,
    login_view,
    logout_view,
    resend_code,
    profile_view,
    edit_profile_view,
    toggle_follow,
)


app_name = "users"

urlpatterns = [
    path("email-verification/", email_verification_view, name="email-verification"),
    path("resend-code/", resend_code, name="resend-code"),
    path("signup/", complete_signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/edit/", edit_profile_view, name="edit-profile"),
    path("profile/<str:username>/", profile_view, name="profile"),
    path("profile/<str:username>/toggle-follow/", toggle_follow, name="toggle-follow"),
]