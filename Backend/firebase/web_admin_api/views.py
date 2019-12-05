from pyfcm import FCMNotification
from rest_framework.response import Response
from rest_framework.views import APIView


class SendNotification(APIView):
    def get(self, request):

        from django.conf import settings

        registration_id = self.request.query_params.get("registration_id", "")

        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        # message_title = "Uber update"
        # message_body = "Hi john, your customized news for today is ready"
        data_message = {"lat": 0, "long": 0}

        result = push_service.notify_single_device(
            registration_id=registration_id, data_message=data_message
        )  # , android_channel_id='cr'

        return Response("ok")
