from django.urls import path, include

app_name = "alerts"

urlpatterns = [
    path("web_admin_api/", include("alerts.web_admin_api.urls")),
    path("mobile_api/", include("alerts.mobile_api.urls")),
]
