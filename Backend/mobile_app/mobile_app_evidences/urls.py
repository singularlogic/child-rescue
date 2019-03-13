from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_evidences'

urlpatterns = [
    path('', EvidenceList.as_view(), name='evidence_list'),
    path('<int:pk>/', EvidenceDetails.as_view(), name='evidence_details'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
