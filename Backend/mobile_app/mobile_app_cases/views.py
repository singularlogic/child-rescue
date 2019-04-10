from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from mobile_app.mobile_app_feedbacks.permissions import HasMobileFeedbackPermission

from core.cases.models import Case, Follower
from .serializers import CaseSerializer


class CaseList(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    #
    # def list(self, request, *args, **kwargs):
    #     latitude = self.request.query_params.get('latitude', None)
    #     longitude = self.request.query_params.get('longitude', None)
    #
    #     if latitude is None or longitude is None:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     return super(CaseList, self).list(request, args, kwargs)
    #
    # def get_queryset(self):
    #     latitude = self.request.query_params.get('latitude', None)
    #     longitude = self.request.query_params.get('longitude', None)
    #
    #     queryset = Case.objects.annotate(
    #         distance=Distance(
    #             'geolocation_point',
    #             Point(float(latitude), float(longitude), srid=4326)
    #         )).order_by('distance')[:2]
    #
    #     result = []
    #     for item in queryset:
    #         print(item.radius)
    #         print(item.distance.km)
    #         if int(item.distance.km) <= item.radius:
    #             result.append(item)
    #
    #     return result


class CaseDetails(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class FollowCase(APIView):
    permission_classes = (HasMobileFeedbackPermission, )

    def post(self, request, *args, **kwargs):

        case_id = kwargs.pop('pk', None)
        if case_id is None or not Case.objects.filter(pk=case_id).exists():
            return Response('You should pass a valid case id', status=status.HTTP_404_NOT_FOUND)

        if request.user is None or request.user.is_anonymous == True:
            return Response('User has no permission', status=status.HTTP_401_UNAUTHORIZED)

        # TODO: update log
        if Follower.objects.filter(case=case_id, user=request.user.id).exists():
            Follower.objects.filter(case=case_id, user=request.user.id).update(is_active=True)
        else:
            Follower.objects.create(case=Case.objects.get(pk=case_id), user=request.user, is_active=True)

        return Response('User is following the case', status=status.HTTP_200_OK)


class UnfollowCase(APIView):
    permission_classes = (HasMobileFeedbackPermission, )

    def post(self, request, *args, **kwargs):

        case_id = kwargs.pop('pk', None)
        if case_id is None or not Case.objects.filter(pk=case_id).exists():
            return Response('You should pass a valid case id', status=status.HTTP_404_NOT_FOUND)

        if request.user is None or request.user.is_anonymous == True:
            return Response('User has no permission', status=status.HTTP_401_UNAUTHORIZED)

        # TODO: update log
        Follower.objects.filter(case=case_id, user=request.user.id).update(is_active=False)

        return Response('User does not follow the case anymore', status=status.HTTP_200_OK)


