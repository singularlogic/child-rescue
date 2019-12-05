from django.urls import path, include

app_name = "firebase"

urlpatterns = [
    path("web_admin_api/", include("firebase.web_admin_api.urls")),
    path("mobile_api/", include("firebase.mobile_api.urls")),
]
