from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", PlaceList.as_view(), name="places_list"),
    path("events/", EventPlaceList.as_view(), name="event_place_list"),
    path("convert/<int:pk>/", ConvertToPlace.as_view(), name="convert_to_place"),
    path("<int:pk>/", PlaceDetails.as_view(), name="place_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
