from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import FCMDeviceCreateOrUpdate, SendNotification

urlpatterns = [
    path('fcm-device-create-or-update/', FCMDeviceCreateOrUpdate.as_view(), name='fcm_device_create_or_update'),
    path('send-test-notification/', SendNotification.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
