from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_cases'

urlpatterns = [
    path('', CaseList.as_view(), name='case_list'),
    path('<int:pk>/', CaseDetails.as_view(), name='case_details'),
    path('<int:pk>/follow_case/', FollowCase.as_view(), name='follow_case'),
    path('<int:pk>/unfollow_case/', UnfollowCase.as_view(), name='unfollow_case'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
