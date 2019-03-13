from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_cases'

urlpatterns = [
    path('', CaseList.as_view(), name='case_list'),
    path('<int:pk>/', CaseDetails.as_view(), name='case_details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)