from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_cases'

urlpatterns = [
    path('<int:pk>/close_case/', CloseCase.as_view(), name='close_case'),
    path('', CaseList.as_view(), name='case_list'),
    path('<int:pk>/', CaseDetails.as_view(), name='case_details'),
    path('upload_image/', UploadImage.as_view(), name='upload_image'),

    path('<int:pk>/archive_case/', ArchiveCase.as_view(), name='archive_case'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
