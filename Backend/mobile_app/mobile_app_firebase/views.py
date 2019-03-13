from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.firebase.models import FCMDevice
from .serializers import FCMDeviceSerializer


class FCMDeviceCreateOrUpdate(APIView):
    serializer_class = FCMDeviceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if 'registration_id' not in request.data:
            return Response({'error': 'registration_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        if 'type' not in request.data:
            return Response({'error': 'type is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            fcm_device = FCMDevice.objects.get(user=user)
        except FCMDevice.DoesNotExist:
            fcm_device = None

        if fcm_device is None:
            return self.create(request, user)
        else:
            return self.update(request, fcm_device)

    def create(self, request, user_instance):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user_instance, active=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, fcm_device):
        serializer = self.serializer_class(fcm_device, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(active=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendNotification(APIView):

    def get(self, request):
        from pyfcm import FCMNotification

        push_service = FCMNotification(api_key='')
        registration_id = 'qweqw'
        message_title = "Uber update"
        message_body = "Hi john, your customized news for today is ready"
        data_message = {
            'action': 0,
            'business_id': 200
        }
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                   message_body=message_body, data_message=data_message,
                                                   sound='Default', badge=1)

        return Response('ok')
