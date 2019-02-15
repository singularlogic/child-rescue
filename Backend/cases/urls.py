from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'cases'

urlpatterns = [
    path('', CaseList.as_view(), name='case_list'),
    path('<int:pk>/', CaseDetails.as_view(), name='case_details'),

    path('profiles/', ProfileList.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileDetails.as_view(), name='case_details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
