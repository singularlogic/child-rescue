from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from feedbacks.web_admin_api.views import FeedbackCountList
from alerts.web_admin_api.views import AlertCountList, AlertAreaCoveredList

urlpatterns = [
    path("feedbacks/count/", FeedbackCountList.as_view(), name="feedback_count_list"),
    path("alerts/count/", AlertCountList.as_view(), name="alert_count_list"),
    path("alerts/area-covered/", AlertAreaCoveredList.as_view(), name="alert_area_covered_list"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
