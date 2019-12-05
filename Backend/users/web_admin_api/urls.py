from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),

    path("me/", UserMe.as_view(), name="me"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot_password"),
    path("reset-password/", PasswordReset.as_view(), name="password_reset"),

    path("", UserList.as_view(), name="get_users"),
    path("<int:pk>/", UserDetail.as_view(), name="user_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
