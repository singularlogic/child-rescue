from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", AlertList.as_view(), name="alert_list"),
    path("<int:pk>/", AlertDetails.as_view(), name="alert_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
