from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from users.mobile_api.views import (
    UserCreate,
    UserLogin,
    UserLogout,
    UserDetail,
    ForgotPassword,
    PasswordReset,
    UuidActivityCreate,
)

urlpatterns = [
    path("register/", UserCreate.as_view(), name="register"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogout.as_view(), name="logout"),
    path("me/", UserDetail.as_view(), name="me"),
    path("<int:pk>/", UserDetail.as_view(), name="user_details"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot_password"),
    path("reset-password/", PasswordReset.as_view(), name="password_reset"),
    path("uuid-activities/", UuidActivityCreate.as_view(), name="uuid_activities_create"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
