import os

from django.conf import settings
import datetime
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from core.cases.models import Case, Child, FacilityHistory, ImageUpload
from core.cases.utils import CaseUtils
from core.alerts.models import Alert
from core.facilities.utils import FacilityUtils
from core.feedbacks.models import Feedback
from .serializers import CaseSerializer, ImageUploadSerializer, CasesSerializer
from django.db.models import F, Q, Subquery
from tzlocal import get_localzone


class UploadImage(APIView):

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if 'image' in request.data and request.data['image'] is not None and request.data['image'] != '':
            image = request.data['image']
            image = CaseUtils.save_image(image)
            request.data['image'] = image
        else:
            content = {'data': 'Invalid data'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            image_object = ImageUpload.objects.create(image=image)
            content = str(image_object.image)
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            content = {'data': 'Invalid serializer'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class CaseList(generics.ListCreateAPIView):
    serializer_class = CasesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        child_id = self.request.query_params.get('child_id', None)
        organization_id = self.request.query_params.get('organization_id', None)
        is_active = self.request.query_params.get('is_active', False)

        # if self.request.user.role is not None and self.request.user.role in ['case_manager']:
        #     pass

        if is_active:
            return Case.get_web_queryset(child_id, organization_id).filter(status='active')
        return Case.get_web_queryset(child_id, organization_id)

    def create(self, request, *args, **kwargs):
        def _has_rights():
            if request.user.role is not None and request.user.role in ['admin', 'owner', 'coordinator', 'case_manager',
                                                                       'network_manager', 'facility_manager']:
                return True
            else:
                return False

        if not _has_rights():
            return Response('User has not an admin role', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)

        if 'child' in request.data and request.data['child'] is not None:
            if not Child.objects.filter(pk=request.data['child']).exists():
                return Response('This child id does not exist', status=status.HTTP_404_NOT_FOUND)

        if 'profile_photo' in request.data and request.data['profile_photo'] is not None and request.data[
            'profile_photo'] != '':
            current_path = settings.MEDIA_ROOT + '/' + request.data['profile_photo']
            if 'tmp/' not in request.data['profile_photo']:
                return Response('Corrupted path', status=status.HTTP_403_FORBIDDEN)
            trash, image_name = request.data['profile_photo'].split('tmp/')
            if not os.path.exists(settings.MEDIA_ROOT + '/' + 'profile_images/'):
                os.makedirs(settings.MEDIA_ROOT + '/' + 'profile_images/')
            target_path = settings.MEDIA_ROOT + '/' + 'profile_images/' + image_name
            os.rename(current_path, target_path)
            media_path = settings.MEDIA_URL + 'profile_images/' + image_name
            request.data['profile_photo'] = media_path

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        demographic_data = self.request.data['demographic_data'] if 'demographic_data' in self.request.data else None
        medical_data = self.request.data['medical_data'] if 'medical_data' in self.request.data else None
        psychological_data = self.request.data[
            'psychological_data'] if 'psychological_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        personal_data = self.request.data['personal_data'] if 'personal_data' in self.request.data else None
        social_media_data = self.request.data['social_media_data'] if 'social_media_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data, medical_data=medical_data,
                        psychological_data=psychological_data, physical_data=physical_data,
                        personal_data=personal_data, social_media_data=social_media_data)

    # if case_search parameter is True, return Active/Inactive/Closed cases
    # only plus the ones that are not present in any facility
    # def get(self, request, *args, **kwargs):
    #
    #     if request.user.role is not None and request.user.role in ['facility_manager']:
    #         facility_id = self.request.query_params.get('facility_id', request.user.facility_id)
    #
    #         if facility_id is None or str(request.user.facility_id) != str(facility_id):
    #             return Response(
    #                 'User does not belong to a facility or has no permission to get data of other facility',
    #                 status=status.HTTP_403_FORBIDDEN)
    #
    #         return Response(FacilityHistory.objects \
    #                         .filter(facility_id=facility_id, is_active=True, case__status='inactive') \
    #                         .annotate(first_name=F('case__personal_data__first_name'),
    #                                   last_name=F('case__personal_data__last_name')) \
    #                         .values('id', 'case__child_id', 'first_name', 'last_name', 'case__profile_photo',
    #                                 'case__status', 'date_entered')
    #                         .distinct('id'))
    #
    #     elif request.user.role is not None and request.user.role in ['case_manager']:
    #
    #         case_search = self.request.query_params.get('case_search', False)
    #         if request.user.organization_id is None:
    #             return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)
    #
    #         if case_search == 'True':
    #             return Response(Case.objects \
    #                             .filter(organization_id=request.user.organization_id,
    #                                     status__in=['active', 'inactive', 'closed']) \
    #                             .filter(
    #                 Q(facility__facilityhistory__isnull=True) | Q(facility__facilityhistory__is_active=False)) \
    #                             .annotate(first_name=F('personal_data__first_name'),
    #                                       last_name=F('personal_data__last_name')) \
    #                             .values('id', 'child_id', 'first_name', 'last_name', 'profile_photo',
    #                                     'status', 'amber_alert')
    #                             .distinct('id'))
    #
    #         return Response(Case.objects \
    #                         .filter(organization_id=request.user.organization_id, status__in=['active', 'closed']) \
    #                         .annotate(first_name=F('personal_data__first_name'),
    #                                   last_name=F('personal_data__last_name')) \
    #                         .values('id', 'child_id', 'first_name', 'last_name', 'profile_photo',
    #                                 'status', 'amber_alert', 'disappearance_type', 'dis')
    #                         .distinct('id'))


class CaseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        def _has_rights():
            if request.user.role is not None and request.user.role in ['admin', 'owner', 'coordinator', 'case_manager',
                                                                       'network_manager', 'facility_manager']:
                return True
            else:
                return False

        if not _has_rights():
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        if request.user.role in ['owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']:
            childs_organization_id = Case.objects.get(pk=kwargs.pop('pk', None)).organization_id
            if request.user.organization_id is None or str(request.user.organization_id) != str(childs_organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if 'profile_photo' in request.data and request.data['profile_photo'] is not None and request.data[
            'profile_photo'] != '' and 'media' not in request.data['profile_photo']:
            if instance.profile_photo:
                path = settings.MEDIA_ROOT + '/' + 'profile_images/' + instance.profile_photo[
                                                                       instance.profile_photo.rindex('/') + 1:]
                os.remove(path)
            current_path = settings.MEDIA_ROOT + '/' + request.data['profile_photo']
            if 'tmp/' not in request.data['profile_photo']:
                return Response('Corrupted path', status=status.HTTP_403_FORBIDDEN)
            trash, image_name = request.data['profile_photo'].split('tmp/')
            if not os.path.exists(settings.MEDIA_ROOT + '/' + 'profile_images/'):
                os.makedirs(settings.MEDIA_ROOT + '/' + 'profile_images/')
            target_path = settings.MEDIA_ROOT + '/' + 'profile_images/' + image_name
            os.rename(current_path, target_path)
            media_path = settings.MEDIA_URL + 'profile_images/' + image_name
            request.data['profile_photo'] = media_path

        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        demographic_data = self.request.data['demographic_data'] if 'demographic_data' in self.request.data else None
        personal_data = self.request.data['personal_data'] if 'personal_data' in self.request.data else None
        medical_data = self.request.data['medical_data'] if 'medical_data' in self.request.data else None
        psychological_data = self.request.data[
            'psychological_data'] if 'psychological_data' in self.request.data else None
        physical_data = self.request.data['physical_data'] if 'physical_data' in self.request.data else None
        social_media_data = self.request.data['social_media_data'] if 'social_media_data' in self.request.data else None

        serializer.save(demographic_data=demographic_data,
                        medical_data=medical_data,
                        psychological_data=psychological_data,
                        physical_data=physical_data,
                        personal_data=personal_data,
                        social_media_data=social_media_data)


class CloseCase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # if not FacilityUtils.has_rights(request.user.role, ['admin', 'coordinator' 'case_manager', 'facility_manager']):
        #     return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        case_id = kwargs.pop('pk', None)

        if case_id is None or not Case.objects.filter(pk=case_id, status__in=['active', 'inactive']).exists():
            return Response('You should pass a valid case id', status=status.HTTP_404_NOT_FOUND)

        if request.user.role in ['coordinator', 'case_manager', 'facility_manager']:
            if request.user.organization_id is None or str(request.user.organization_id) != str(Case.objects.get(pk=case_id).organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        # TODO: inform followers
        # TODO: update log
        # close active alerts
        local_now = datetime.datetime.now(get_localzone())
        case = Case.objects.get(pk=case_id)
        if case.status == 'active':
            Alert.objects.filter(case_id=case_id, is_active=True).update(is_active=False)

        # if the child was living in facility
        # elif case.status == 'inactive':
        #     FacilityHistory.objects.filter(case_id=case_id, is_active=True).update(is_active=False, date_left=local_now)

        # change status
        # change is_present/date_left in facility
        case.status = 'closed'
        case.save()

        return Response('Case {} closed'.format(case_id), status=status.HTTP_200_OK)


class ArchiveCase(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not FacilityUtils.has_rights(request.user.role,
                                        ['admin', 'coordinator', 'case_manager', 'facility_manager']):
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        case_id = kwargs.pop('pk', None)

        if case_id is None or not Case.objects.filter(pk=case_id, status__in=['active', 'inactive', 'closed']).exists():
            return Response('You should pass a valid/not archived case id', status=status.HTTP_404_NOT_FOUND)

        if request.user.role in ['coordinator', 'case_manager', 'facility_manager']:
            if request.user.organization_id is None or str(request.user.organization_id) != str(
                Case.objects.get(pk=case_id).organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        # close active alerts
        # TODO: update log
        local_now = datetime.datetime.now(get_localzone())
        case = Case.objects.get(pk=case_id)
        case.status = 'archived'
        case.save()

        Alert.objects.filter(case_id=case_id, is_active=True).update(is_active=False)

        # if the child was living in facility, change is_present/date_left in facility
        # TODO: update log
        FacilityHistory.objects.filter(case_id=case_id, is_active=True).update(is_active=False, date_left=local_now)

        return Response('Case {} archived'.format(case_id), status=status.HTTP_200_OK)
