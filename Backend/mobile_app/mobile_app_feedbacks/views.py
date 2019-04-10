from rest_framework import generics, status

from core.feedbacks.models import Feedback
from core.users.models import User
from mobile_app.mobile_app_feedbacks.permissions import HasMobileFeedbackPermission
from .serializers import FeedbackSerializer
from rest_framework.response import Response
from django.db.models import F


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (HasMobileFeedbackPermission, )

    def get(self, request, *args, **kwargs):

        user_id = request.user.id
        if user_id is None or not User.objects.filter(pk=user_id).exists():
            return Response('User Id is invalid or User does not exist', status=status.HTTP_403_FORBIDDEN)

        return Response(Feedback.objects.filter(user=user_id)\
                        .annotate(child_id=F('case__child_id'))
                        .values('id', 'alert_id', 'child_id', 'comment', 'created_at')\
                        .distinct('id'))

    def create(self, request, *args, **kwargs):
        # add extra fields before hitting the serializer
        if not request.data._mutable:
            request.data._mutable = True
        if request.user.is_anonymous:
            request.data['source'] = 'Anonymous'
        else:
            request.data['source'] = "{} {}".format(self.request.user.first_name, self.request.user.last_name)

        if 'current_latitude' not in request.data or 'current_longitude' not in request.data:
            return Response('Current latitude/current longitude is required', status=status.HTTP_403_FORBIDDEN)

        if 'latitude' not in request.data or 'longitude' not in request.data:
            request.data['latitude'] = request.data['current_latitude']
            request.data['longitude'] = request.data['current_longitude']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeedbackDetails(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (HasMobileFeedbackPermission,)
