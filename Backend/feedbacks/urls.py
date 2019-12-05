from django.urls import path, include

app_name = "feedbacks"

urlpatterns = [
    path("web_admin_api/", include("feedbacks.web_admin_api.urls")),
    path("mobile_api/", include("feedbacks.mobile_api.urls")),
]
