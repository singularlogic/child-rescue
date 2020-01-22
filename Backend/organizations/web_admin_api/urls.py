from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", OrganizationList.as_view(), name="organization_list"),
    path("<int:pk>/", OrganizationDetails.as_view(), name="organization_details"),
    path("<int:pk>/users/", OrganizationUsersList.as_view(), name="organization_users"),
    path("users-create/", OrganizationUsersCreate.as_view(), name="organization_user_create"),
    path("<int:pk>/user/", OrganizationUserDetails.as_view(), name="organization_user_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
