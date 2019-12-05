from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import SendNotification

urlpatterns = [path("send-test-notification/", SendNotification.as_view())]

urlpatterns = format_suffix_patterns(urlpatterns)
