from django.urls import path, include

app_name = "places"

urlpatterns = [
    path("web_admin_api/", include("places.web_admin_api.urls")),
    # path("mobile_api/", include("places.mobile_api.urls")),
]
