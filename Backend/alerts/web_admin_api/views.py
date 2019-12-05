from django.conf import settings
from django.contrib.gis.geos import Point
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from alerts.web_admin_api.permissions import (
    HasAlertOrganizationAdminPermissions,
    HasCreateAlertPermissions,
    HasGetAlertPermissions,
    HasDeleteAlertPermissions,
)
from alerts.web_admin_api.serializers import AlertSerializer
from firebase.models import FCMDevice
from firebase.pyfcm.fcm import FCMNotification
from organizations.models import Organization
from users.web_admin_api.permissions import (
    HasCaseManagerPermissions,
    HasGeneralAdminPermissions,
)


class LatestAlertList(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = (HasGeneralAdminPermissions,)

    def get_queryset(self):
        return Alert.objects.get_latest_web_queryset(self.request.user.organization_id)


class AlertList(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = (
        HasCaseManagerPermissions,
        HasCreateAlertPermissions,
        HasGetAlertPermissions,
    )

    @staticmethod
    def send_notification(data):
        data_message = {
            "type": "alert_notification",
            "title": data["fullname"],
            "description": data["description"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "radius": data["radius"],
        }
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        devices = FCMDevice.objects.all()
        registration_ids = []
        for device in devices:
            if device is not None and device.active is True:
                registration_ids.append(device.registration_id)
        try:
            push_service.notify_multiple_devices(
                registration_ids=registration_ids,
                # message_title=title,
                # message_body=description,
                data_message=data_message,
                android_channel_id="cr",
                # sound='Default',
                # badge=1
            )
        except Exception as exception:
            print(exception)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        case_id = self.request.query_params.get("caseId", None)
        active = self.request.query_params.get("is_active", None)
        if organization_id is None:
            organization_id = self.request.query_params.get("organization_id", None)
        return Alert.objects.get_web_queryset(active, case_id, organization_id)

    def perform_create(self, serializer):
        organization = Organization.objects.get(id=self.request.user.organization_id)
        geolocation_point = Point(float(self.request.data["latitude"]), float(self.request.data["longitude"]))
        serializer.save(geolocation_point=geolocation_point, organization=organization)
        self.send_notification(serializer.data)


class AlertDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (
        HasCaseManagerPermissions,
        HasAlertOrganizationAdminPermissions,
        HasDeleteAlertPermissions,
    )

    def destroy(self, request, *args, **kwargs):
        alert_id = kwargs.pop("pk", None)
        instance = Alert.objects.get(id=alert_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeactivateAlert(APIView):
    permission_classes = (
        HasCaseManagerPermissions,
        HasAlertOrganizationAdminPermissions,
    )

    @staticmethod
    def post(request, *args, **kwargs):
        alert_id = kwargs.pop("pk", None)
        return Alert.objects.deactivate(alert_id)