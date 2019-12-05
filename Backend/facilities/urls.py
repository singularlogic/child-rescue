from django.urls import path, include

app_name = "facilities"

urlpatterns = [
    path("web_admin_api/", include("facilities.web_admin_api.urls")),
    # path('mobile_api/', include('facilities.mobile_api.urls')),
]
