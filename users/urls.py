from django.urls import path
from .views import request_code, verify_code, complete_signup, login_view, logout_view, resend_code


app_name = "users"

urlpatterns = [
    path("request-code/", request_code, name="request-code"),
    path("verify-code/", verify_code, name="verify-code"),
    path("signup/", complete_signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("resend-code/", resend_code, name="resend-code"),
]