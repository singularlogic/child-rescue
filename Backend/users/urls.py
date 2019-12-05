from django.urls import path, include

app_name = "users"

urlpatterns = [
    path("web_admin_api/", include("users.web_admin_api.urls")),
    path("mobile_api/", include("users.mobile_api.urls")),
]
