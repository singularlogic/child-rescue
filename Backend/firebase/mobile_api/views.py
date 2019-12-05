from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from firebase.models import FCMDevice
from users.models import Uuid
from .serializers import FCMDeviceSerializer


class FCMDeviceCreateOrUpdate(APIView):
    serializer_class = FCMDeviceSerializer

    def post(self, request, *args, **kwargs):

        if "uuid" not in request.data:
            return Response(
                {"error": "uuid is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if "registration_id" not in request.data:
            return Response(
                {"error": "registration_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "type" not in request.data:
            return Response(
                {"error": "type is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        uuid = Uuid.objects.filter(value=request.data["uuid"]).first()
        if uuid is None:
            uuid = Uuid.objects.create(value=request.data["uuid"])

        try:
            fcm_device = FCMDevice.objects.get(uuid=uuid)
        except FCMDevice.DoesNotExist:
            fcm_device = None

        if fcm_device is None:
            return self.create(request, uuid)
        else:
            return self.update(request, fcm_device)

    def create(self, request, uuid_instance):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uuid=uuid_instance, active=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, fcm_device):
        serializer = self.serializer_class(fcm_device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(active=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
