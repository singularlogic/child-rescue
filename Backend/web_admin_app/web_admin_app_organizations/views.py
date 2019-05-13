from rest_framework import permissions, generics, status, viewsets
from rest_framework.views import APIView

from core.organizations.models import Organization
from core.users.models import User
from core.cases.models import FacilityHistory
from .serializers import OrganizationSerializer
from core.facilities.utils import FacilityUtils
from tzlocal import get_localzone
from django.db.models import Q, F

from rest_framework.response import Response
import datetime


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrganizationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        if request.user.role == 'owner':
            if request.user.organization_id is None:
                return Response('Owner does not belong to an organization', status=status.HTTP_403_FORBIDDEN)
            if request.user.organization_id != kwargs.pop('pk', None):
                return Response('Owner does not have permission to edit details', status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        if request.user.role == 'owner':
            if request.user.organization_id is None:
                return Response('Owner does not belong to an organization', status=status.HTTP_403_FORBIDDEN)
            if request.user.organization_id != kwargs.pop('pk', None):
                return Response('Owner does not have permission to edit details', status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class OrganizationCompleteness(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        organization_id = kwargs.pop('pk', None)
        if organization_id is None:
            return Response('User does not have permission', status=status.HTTP_404_NOT_FOUND)

        facilityId = self.request.query_params.get('facility_id', None)

        local_now = datetime.datetime.now(get_localzone())
        result = FacilityHistory.objects \
            .filter(is_active=True) \
            .filter(case__facility__organization_id=organization_id) \
            .filter(date_entered__lt=local_now) \
            .filter(Q(date_left__isnull=True) | Q(date_left__gt=local_now))
        if facilityId is not None:
            result = result.filter(facility_id=facilityId)

        result = result \
            .annotate(child_id=F('case__child_id'), first_name=F('case__personal_data__first_name'),
                      last_name=F('case__personal_data__last_name'), facility_name=F('facility__name'),
                      organization_name=F('facility__organization__name'))\
            .distinct('id') \
            .values('child_id', 'first_name', 'last_name', 'facility_name', 'organization_name')

        return Response(result)


# get organization users
class OrganizationUsers(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        organization_id = kwargs.pop('pk', None)
        if organization_id is None:
            return Response('We should pass a valid organization id', status=status.HTTP_404_NOT_FOUND)

        list_of_roles = ['owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']
        result = User.objects.filter(organization_id=organization_id, role__in=list_of_roles)\
            .annotate(organization_name=F('organization__name'), facility_name=F('facility__name'))\
            .values('id', 'role', 'first_name', 'last_name', 'organization_name', 'facility_name')

        return Response(result)


class RemoveOrganizationUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        # Check if the user has access on this organization
        organization_id = kwargs.pop('pk', None)
        if request.user.organization_id is None or str(request.user.organization_id) != str(organization_id):
            return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user exists + on this organization
        user_id = self.request.query_params.get('user_id', None)
        if user_id is None or not User.objects.filter(pk=user_id, organization_id=organization_id, is_active=True).exists():
            return Response('The User you want to remove does not exist in this organization', status=status.HTTP_401_UNAUTHORIZED)

        # Check if the user tries to delete himself
        if user_id == str(request.user.id):
            return Response('You cannot remove yourself from the organization', status=status.HTTP_401_UNAUTHORIZED)

        # Remove the user from the organization (is_active=False)
        User.objects.filter(pk=user_id).update(is_active=False)

        return Response('User is removed from the organization', status=status.HTTP_202_ACCEPTED)

