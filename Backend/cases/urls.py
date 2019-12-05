from django.urls import path, include

app_name = "cases"

urlpatterns = [
    path("web_admin_api/", include("cases.web_admin_api.urls")),
    path("mobile_api/", include("cases.mobile_api.urls")),
]
