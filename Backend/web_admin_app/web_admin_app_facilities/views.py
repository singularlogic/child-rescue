
import datetime
from rest_framework import permissions, generics, status
from django.http.response import JsonResponse

from rest_framework.response import Response

from core.facilities.models import Facility
from core.users.models import User
from core.cases.models import Case, Child, FacilityHistory
from .serializers import FacilitySerializer
from rest_framework.views import APIView
from django.db.models import Q, F
from core.facilities.utils import FacilityUtils

from tzlocal import get_localzone


class FacilityList(generics.ListCreateAPIView):

    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'owner' or request.user.role == 'coordinator':
            return Response(Facility.objects \
                            .filter(organization_id=request.user.organization_id) \
                            .annotate(organization_name=F('organization__name'))
                            .values('id', 'name', 'organization_name', 'supports_hosting', 'capacity'))

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        has_organization_attached = 'organization' in request.data and request.data['organization'] is not None and len(request.data['organization']) > 0

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'owner' or request.user.role == 'coordinator':
            if not has_organization_attached or str(request.user.organization_id) != request.data['organization']:
                return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        return self.create(request, *args, **kwargs)


class FacilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        has_organization_attached = 'organization' in request.data and request.data['organization'] is not None and len(request.data['organization']) > 0

        facility_id = kwargs.pop('pk', None)
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'owner' or request.user.role == 'coordinator':
            if request.user.organization_id is None:
                return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

            if Facility.objects.get(pk=facility_id).organization_id != request.user.organization_id:
                return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

            # Do not allow the User to change organization
            if has_organization_attached:
                return Response('User has no permission to change organization', status=status.HTTP_403_FORBIDDEN)

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        has_organization_attached = 'organization' in request.data and request.data['organization'] is not None and len(request.data['organization']) > 0

        facility_id = kwargs.pop('pk', None)
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'owner' or request.user.role == 'coordinator':
            if request.user.organization_id is None:
                return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

            if Facility.objects.get(pk=facility_id).organization_id != request.user.organization_id:
                return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

            # Do not allow the User to change organization
            if has_organization_attached:
                return Response('User has no permission to change organization', status=status.HTTP_403_FORBIDDEN)

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        facility_id = kwargs.pop('pk', None)
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role == 'owner' or request.user.role == 'coordinator':
            if request.user.organization_id is None:
                return Response('User does not belong to an organization', status=status.HTTP_403_FORBIDDEN)

            if Facility.objects.get(pk=facility_id).organization_id != request.user.organization_id:
                return Response('User has access only to the facilities he belongs', status=status.HTTP_403_FORBIDDEN)

        if User.objects.filter(facility_id=facility_id).count() > 0:
            return Response('There are one or more users attached to this facility', status=status.HTTP_403_FORBIDDEN)

        return self.destroy(request, *args, **kwargs)


def get_num_of_occupiers(facility_id):

    local_now = datetime.datetime.now(get_localzone())
    return FacilityHistory.objects\
            .filter(facility_id=facility_id, is_active=True, date_entered__lt=local_now)\
            .filter(Q(date_left__isnull=True) | Q(date_left__gt=local_now))\
            .count()


class FacilityCompleteness(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        facility_id = kwargs.pop('pk', None)
        if facility_id is None:
            return Response('We should pass a valid facility id', status=status.HTTP_404_NOT_FOUND)

        dict = {}
        dict['capacity'] = Facility.objects.get(pk=facility_id).capacity
        dict['occupants'] = get_num_of_occupiers(facility_id)

        return JsonResponse(dict)


class FacilityRemoveChild(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager', 'facility_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        facility_id = kwargs.pop('pk', None)
        if facility_id is None:
            return Response('We should pass a valid facility id', status=status.HTTP_404_NOT_FOUND)

        if request.user.facility_id is None or \
            request.user.organization_id is None or \
            Facility.objects.filter(organization_id=request.user.organization_id, pk=facility_id).count() == 0:
            return Response('There are no facilities in the Users organization', status=status.HTTP_404_NOT_FOUND)

        child_id = self.request.query_params.get('child_id', None)
        if child_id is None:
            return Response('We should pass a valid child id', status=status.HTTP_404_NOT_FOUND)

        cases_objects = FacilityHistory.objects.filter(case__child_id=child_id, facility_id=facility_id)
        if not cases_objects.exists():
            return Response('This child was never accommodated in this facility', status=status.HTTP_404_NOT_FOUND)

        if not cases_objects.filter(case__status='active', is_active=True, date_left__isnull=True).exists():
            return Response('This child is not living in the facility at the moment', status=status.HTTP_404_NOT_FOUND)

        active_fac_history = cases_objects.get(case__status='active', is_active=True, date_left__isnull=True)
        local_now = datetime.datetime.now(get_localzone())
        to_datetime = self.request.query_params.get('to_datetime', local_now)
        active_fac_history.date_left = to_datetime
        active_fac_history.is_active = False
        active_fac_history.save()

        return Response('The record of the child with id {} was updated'.format(child_id), status=status.HTTP_200_OK)


class FacilityAddChild(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager', 'facility_manager']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        organization_id = self.request.query_params.get('organization_id', None)
        facility_id = self.request.query_params.get('facility_id', None)
        child_id = self.request.query_params.get('child_id', None)

        # 1. check if HFM has access to this facility/organization
        if request.user.role in ['owner', 'coordinator', 'case_manager', 'facility_manager']:
            if request.user.organization_id is None or str(request.user.organization_id) != organization_id:
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

            if request.user.role in ['case_manager', 'facility_manager']:
                if request.user.facility_id is None or str(request.user.facility_id) != facility_id:
                    return Response('User has no permission to this facility', status=status.HTTP_401_UNAUTHORIZED)

        # 2. check if the child exists
        if not Child.objects.filter(pk=child_id, case__status='active', case__organization=organization_id).exists():
            return Response('Child does not exist / has no active case in the organizations database', status=status.HTTP_404_NOT_FOUND)

        # 3. check if facility exists in organization and is a hosting facility
        if not Facility.objects.filter(pk=facility_id, organization_id=organization_id, supports_hosting=True, is_active=True).exists():
            return Response('Facility does not exist / is not part of the organization / is not active / does not support hosting', status=status.HTTP_404_NOT_FOUND)

        local_now = datetime.datetime.now(get_localzone())
        from_datetime = self.request.query_params.get('from_datetime', local_now)
        case = Case.objects.get(child_id=child_id, status='active')

        # 4. check if the child is already registered in the facility
        if FacilityHistory.objects.filter(facility_id=facility_id, case_id=case.id, date_left__isnull=True).exists():
            return Response('This child is already registered in this facility', status=status.HTTP_406_NOT_ACCEPTABLE)

        # 5. check if there is space in the facility
        num_of_occupiers = get_num_of_occupiers(facility_id)
        capacity = Facility.objects.get(pk=facility_id).capacity

        if num_of_occupiers >= capacity:
            return Response('Facility cannot accommodate any more children', status=status.HTTP_406_NOT_ACCEPTABLE)

        # create entry
        FacilityHistory.objects.create(facility=Facility.objects.get(pk=facility_id), case=case, date_entered=from_datetime, is_active=True)

        return Response('The child id {} was added to the facility {}'.format(child_id, facility_id), status=status.HTTP_200_OK)


# Admin/Owner/Coordinator should be able to attach hosting facility manager to a facility
class FacilityAssignHFM(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator']):
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        # 0. check parameters (user_id, facility_id) => extract organization_id
        user_id = self.request.query_params.get('user_id', None)
        facility_id = self.request.query_params.get('facility_id', None)

        if user_id is None or facility_id is None:
            return Response('User and Facility parameters are required', status=status.HTTP_403_FORBIDDEN)

        organization_id = self.request.query_params.get('organization_id', Facility.objects.get(pk=facility_id).organization_id)

        # 1.1 if its owner/coordinator, check if the organization he belongs is the same as the one to assign to
        # 1.2 check if the facility belongs to this organization
        if request.user.role in ['owner', 'coordinator']:
            if request.user.organization_id is None or str(request.user.organization_id) != str(organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        # 1.3 if the facility does not belong to the organization or its inactive
        if not Facility.objects.filter(pk=facility_id, organization_id=organization_id, is_active=True).exists():
            return Response('This Facility does not belong to this organization or is not Active', status=status.HTTP_401_UNAUTHORIZED)

        # 2. check if user is HFM
        user = User.objects.get(pk=user_id)
        if user.role is not None and user.role != 'facility_manager':
            return Response('User role is not Hosting Facility Manager', status=status.HTTP_403_FORBIDDEN)

        # 3. check if user is HFM and belongs to this organization
        user = User.objects.get(pk=user_id)
        if user.organization_id is None or str(user.organization_id) != str(organization_id):
            return Response('User belongs to a different organization', status=status.HTTP_403_FORBIDDEN)

        # 4. check if HFM is already member of this facility
        if str(user.facility_id) == facility_id:
            return Response('User id {} already belongs to the facility id {}'.format(user_id, facility_id), status=status.HTTP_403_FORBIDDEN)

        # 5. Assign
        user.facility_id = facility_id
        user.organization_id = organization_id
        user.save()

        return Response('User id {} was assigned to the facility id {}'.format(user_id, facility_id), status=status.HTTP_200_OK)
