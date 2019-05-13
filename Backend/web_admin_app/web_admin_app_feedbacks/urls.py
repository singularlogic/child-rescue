from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'web_admin_app_feedbacks'

urlpatterns = [
    path('', FeedbackList.as_view(), name='feedback_list'),
    path('<int:pk>/', FeedbackDetails.as_view(), name='feedback_details'),
    # path('<int:pk>/feedback_approval/', FeedbackApproval.as_view(), name='feedback_approval'),
    path('upload_image/', UploadImage.as_view(), name='upload_image'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
