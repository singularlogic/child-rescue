from rest_framework import permissions, generics
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.alerts.models import Alert
from web_admin_app.web_admin_app_alerts.serializers import AlertSerializer


class AlertList(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):

        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)

        if latitude is None or longitude is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return super(AlertList, self).list(request, args, kwargs)

    def get_queryset(self):

        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)

        return Alert.objects.get_mobile_queryset(latitude, longitude)


class AlertDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated,)
