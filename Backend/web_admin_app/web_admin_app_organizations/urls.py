from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_organizations'

urlpatterns = [
    path('', OrganizationList.as_view(), name='organization_list'),
    path('<int:pk>/', OrganizationDetails.as_view(), name='organization_details'),
    path('<int:pk>/completeness/', OrganizationCompleteness.as_view(), name='organization_completeness'),
    path('<int:pk>/get_users/', OrganizationUsers.as_view(), name='organization_users'),
    path('<int:pk>/remove_user_from_organization/', RemoveOrganizationUser.as_view(), name='remove_organization_user'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
