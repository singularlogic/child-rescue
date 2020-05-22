from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = [
    path("", CaseList.as_view(), name="case_list"),
    path("<int:pk>/", CaseDetails.as_view(), name="case_details"),
    path("volunteer-cases/", VolunteerCasesList.as_view(), name="volunteer_cases_list"),
    path("<int:pk>/accept-invite/", AcceptInvite.as_view(), name="accept_invite"),
    path("<int:pk>/decline-invite/", DeclineInvite.as_view(), name="decline_invite"),
    path(
        "<int:pk>/update-location/",
        VolunteerCasesLocation.as_view(),
        name="volunteer_cases_location",
    ),
    path("<int:pk>/feed/", FeedList.as_view(), name="feed_list"),
    path("<int:pk>/my-feed/", MyFeedList.as_view(), name="feed_list"),
    path("<int:pk>/volunteers/", VolunteerList.as_view(), name="volunteer_list"),
    path("followed-cases/", FollowedCases.as_view(), name="followed_cases"),
    path("<int:pk>/follow/", FollowCase.as_view(), name="follow"),
    path("<int:pk>/unfollow/", UnfollowCase.as_view(), name="unfollow"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
