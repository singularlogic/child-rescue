from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", FacilityList.as_view(), name="facility_list"),
    path("<int:pk>/", FacilityDetail.as_view(), name="facility_details"),
    path(
        "add_child_in_facility/<int:child_id>/",
        FacilityAddChild.as_view(),
        name="add_child_in_facility",
    ),
    path(
        "remove_child_from_facility/<int:child_id>/",
        FacilityRemoveChild.as_view(),
        name="remove_child_from_facility",
    ),
    path(
        "<int:pk>/add_manager/<int:user_id>/",
        FacilityAddManager.as_view(),
        name="facility_add_manager",
    ),
    path(
        "<int:pk>/remove_manager/<int:user_id>/",
        FacilityRemoveManager.as_view(),
        name="facility_remove_manager",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
