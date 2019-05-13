from django.contrib.gis.geos import Point
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.alerts.models import Alert
from web_admin_app.web_admin_app_alerts.serializers import AlertSerializer
from core.facilities.utils import FacilityUtils


class AlertList(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        case_id = self.request.query_params.get('caseId', None)
        active = self.request.query_params.get('active', None)

        return Alert.objects.get_web_queryset(active, case_id)  # .order_by('disappearance_date')

    def create(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        geolocation_point = Point(float(self.request.data['latitude']), float(self.request.data['longitude']))
        serializer.save(geolocation_point=geolocation_point)


class AlertDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role in ['owner', 'coordinator', 'case_manager']:
            alert_organization = Alert.objects.get(pk=kwargs.pop('pk', None)).case.organization_id
            if request.user.organization_id is None or str(request.user.organization_id) != str(alert_organization):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        alert_id = kwargs.pop('pk', None)
        return Alert.objects.deactivate(alert_id)


class DeactivateAlert(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
            return Response('User has not an admin role', status=status.HTTP_403_FORBIDDEN)

        alert_id = kwargs.pop('pk', None)
        # 1. check if its admin belongs in the same organization as the one to assign the alert belongs to
        if request.user.role in ['owner', 'coordinator']:
            if request.user.organization_id is None or str(request.user.organization_id) != str(Alert.objects.get(pk=alert_id).case.organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        return Alert.objects.deactivate(alert_id)

