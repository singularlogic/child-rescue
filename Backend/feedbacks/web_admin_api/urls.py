from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", FeedbackList.as_view(), name="feedback_list"),
    path("latest/", LatestFeedbackList.as_view(), name="latest_feedback_list"),
    path("<int:pk>/", FeedbackDetails.as_view(), name="feedback_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
