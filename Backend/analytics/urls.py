from django.urls import path, include

app_name = "analytics"

urlpatterns = [path("web_admin_api/", include("analytics.web_admin_api.urls"))]
