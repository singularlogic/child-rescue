from rest_framework import generics, status
from rest_framework.response import Response

from alerts.mobile_api.serializers import AlertSerializer
from alerts.models import Alert
from users.uuid_management import UuidManagement


class AlertList(generics.ListAPIView):
    serializer_class = AlertSerializer

    def get_queryset(self):

        latitude = self.request.query_params.get("latitude", None)
        longitude = self.request.query_params.get("longitude", None)

        if latitude is None or longitude is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        uuid = self.request.query_params.get("uuid", None)
        if uuid is not None:
            action = "get_alerts"
            params = self.request.query_params.get("params", "")
            device = self.request.query_params.get("device", "")
            UuidManagement.log_action(self.request, uuid, action, params, device)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Alert.objects.get_mobile_queryset(latitude, longitude)


class AlertDetails(generics.RetrieveAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
