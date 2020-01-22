from django.urls import path, include

app_name = "organizations"

urlpatterns = [
    path("web_admin_api/", include("organizations.web_admin_api.urls")),
    path("mobile_api/", include("organizations.mobile_api.urls")),
]
