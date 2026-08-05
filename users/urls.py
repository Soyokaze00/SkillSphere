from django.urls import path

from .views import (
    complete_signup,
    delete_account_view,
    edit_profile_view,
    email_verification_view,
    login_view,
    logout_view,
    profile_view,
    resend_code,
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
    path("profile/delete/", delete_account_view, name="delete-account"),
    path("profile/<str:username>/", profile_view, name="profile"),
    path("profile/<str:username>/toggle-follow/", toggle_follow, name="toggle-follow"),
]
