import datetime
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.alerts.models import Alert
from core.cases.models import Case
from core.feedbacks.models import Feedback, ImageUpload
from core.facilities.utils import FacilityUtils
from core.users.models import User
from .serializers import FeedbackSerializer, ImageUploadSerializer
from tzlocal import get_localzone
from core.cases.utils import CaseUtils


class FeedbackList(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        case_id = self.request.query_params.get('caseId', None)

        if case_id is not None:
            queryset = Feedback.objects.filter(case=case_id).order_by('id').reverse()
        else:
            queryset = Feedback.objects.all().order_by('id').reverse()
            # return Response('No case id given', status=status.HTTP_403_FORBIDDEN)
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Case manager will upload feedback always with no alert id
        case_id = self.request.data['case'] if 'case' in self.request.data else None
        alert_id = self.request.data['alert'] if 'alert' in self.request.data else None

        if self.request.data['feedback_status'] != 'pending':
            checked_by_id = self.request.user.id
            checked_on = datetime.datetime.now(get_localzone())
            serializer.save(
                case=Case.objects.get(id=case_id),
                user=self.request.user,
                checked_by_id=checked_by_id,
                checked_on=checked_on
            )
        else:
            serializer.save(
                case=Case.objects.get(id=case_id),
                user=self.request.user,
            )

        # if alert_id is not None:
        #     serializer.save(
        #         case=Case.objects.get(id=case_id),
        #         user=self.request.user,
        #         alert=Alert.objects.get(id=alert_id),
        #     )
        # else:
        #     serializer.save(
        #         case=Case.objects.get(id=case_id),
        #         user=self.request.user,
        #     )


class FeedbackDetails(generics.RetrieveUpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
        return self.retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        def _has_rights():
            if request.user.role is not None and request.user.role in ['admin', 'owner', 'coordinator', 'case_manager',
                                                                       'network_manager']:
                return True
            else:
                return False

        if not _has_rights():
            return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        if request.user.role in ['owner', 'coordinator', 'case_manager', 'network_manager', 'facility_manager']:
            if request.user.organization_id is None or str(request.user.organization_id) != str(
                instance.case.organization_id):
                return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)

        # if (instance.feedback_status is None or instance.feedback_status == 'pending') \
        #     and request.data['feedback_status'] != 'pending':
        #     instance.checked_by = self.request.user
        #     instance.checked_on = datetime.datetime.now(get_localzone())

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        if (instance.feedback_status is None or instance.feedback_status == 'pending') \
            and self.request.data['feedback_status'] != 'pending':
            checked_by_id = self.request.user.id
            checked_on = datetime.datetime.now(get_localzone())
            serializer.save(checked_by_id=checked_by_id, checked_on=checked_on)
        else:
            serializer.save()

    # def put(self, request, *args, **kwargs):
    #     if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
    #         return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
    #     return self.update(request, *args, **kwargs)
    #
    # def patch(self, request, *args, **kwargs):
    #     if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
    #         return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
    #     return self.partial_update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     if request.user.role not in ['owner', 'coordinator', 'case_manager', 'network_manager']:
    #         return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
    #     return self.destroy(request, *args, **kwargs)


# Admin/Owner/Coordinator should be able to attach hosting facility manager to a facility
# class FeedbackApproval(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         if not FacilityUtils.has_rights(request.user.role, ['admin', 'owner', 'coordinator', 'case_manager']):
#             return Response('User has no permission', status=status.HTTP_403_FORBIDDEN)
#
#         # 0. check parameters (feedback_id)
#         feedback_id = kwargs.pop('pk', None)
#         feedback_status = self.request.query_params.get('feedback_status', None)
#         local_now = datetime.datetime.now(get_localzone())
#
#         if feedback_id is None:
#             return Response('Feedback parameter is required', status=status.HTTP_403_FORBIDDEN)
#
#         feedback = Feedback.objects.get(pk=feedback_id)
#
#         # 1.1 if he is not an admin, check if the organization he belongs is the same as the one to assign to
#         # 1.2 check if the facility belongs to this organization
#         if request.user.role in ['owner', 'coordinator', 'case_manager']:
#             if request.user.organization_id is None or str(request.user.organization_id) != str(
#                 feedback.case.organization_id):
#                 return Response('User has no permission to this organization', status=status.HTTP_401_UNAUTHORIZED)
#
#         # 2. check if feedback is already approved
#         # if feedback.checked_on is not None:
#         #     return Response('Feedback {} was already checked on {}'.format(feedback.id, feedback.checked_on),
#         #                     status=status.HTTP_403_FORBIDDEN)
#
#         # 3. Update
#         feedback.checked_on = local_now
#         feedback.checked_by = request.user
#         feedback.feedback_status = feedback_status
#         feedback.save()
#
#         return Response('The feedback {} was checked by {}'.format(feedback.id, feedback.checked_by),
#                         status=status.HTTP_200_OK)


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
