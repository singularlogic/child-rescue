from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", OrganizationList.as_view(), name="organization_list"),
    path("<int:pk>/", OrganizationDetails.as_view(), name="organization_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
