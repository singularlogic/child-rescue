import os
import datetime

from PIL import Image
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from analytics.analytics_basic import IntelliSearch
from blockchain.blockchain import changeStatus
from cases.models import FacilityHistory, Case, Follower, CaseVolunteer, File, Feed, Child, SocialMedia
from cases.utils import CaseUtils
from cases.web_admin_api.permissions import (
    FacilityCaseStatePermissions,
    HasCaseOrganizationAdminPermissions,
    HasCreateCasesPermissions,
    HasCloseCasePermissions,
    HasFilePermissions,
    HasArchiveCasePermissions,
)
from firebase.models import FCMDevice
from firebase.pyfcm import FCMNotification
from users.models import Uuid, User
from users.web_admin_api.permissions import (
    HasGeneralAdminPermissions,
    HasCaseManagerPermissions,
)
from .serializers import (
    # CaseSerializer,
    CasesSerializer,
    CaseVolunteerSerializer,
    FileSerializer,
    FeedSerializer,
    ChildSerializer,
    SocialMediaSerializer,
)
from tzlocal import get_localzone


class ChildrenList(APIView):
    def get(self, request, **kwargs):
        name = request.query_params.get("name", None)
        queryset = IntelliSearch().run_rawsql_namesearch(name, request.user.organization_id)
        formatted_response = list()
        for child in queryset:
            formatted_response.append(
                {
                    "id": child[0],
                    "first_name": child[1],
                    "last_name": child[2],
                    "case_id": child[3],
                    "status": child[4],
                    "rank": child[5],
                }
            )
        return Response(formatted_response)


class ChildDetails(generics.RetrieveAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    # permission_classes = (HasFilePermissions, )

    @staticmethod
    def send_notification(registration_ids, title, case_id):
        data_message = {"type": "post_notification", "title": title, "case_id": case_id}
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        try:
            push_service.notify_multiple_devices(
                registration_ids=registration_ids,
                # message_title=title,
                # message_body=description,
                data_message=data_message,
                android_channel_id="cr",
                # sound='Default',
                # badge=1
            )
        except Exception as exception:
            print(exception)

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        queryset = Feed.objects.filter(case=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # if not request.data._mutable:
        #     request.data._mutable = True
        request.data["user"] = request.user.id
        request.data["case"] = kwargs.get("pk")
        case = get_object_or_404(Case, id=kwargs["pk"])
        case_volunteers = CaseVolunteer.objects.filter(case=case)
        registration_ids = []
        for case_volunteer in case_volunteers:
            uuids = Uuid.objects.filter(user=case_volunteer.user)
            if len(uuids) <= 0:
                return Response("Account not activated yet!", status=status.HTTP_204_NO_CONTENT)
            devices = FCMDevice.objects.filter(uuid__in=uuids)
            for device in devices:
                registration_ids.append(device.registration_id)
            if len(registration_ids) <= 0:
                return Response("Account's firebase token not exists!", status=status.HTTP_204_NO_CONTENT)
        title = "New post for case: {}".format(case.custom_name)
        if request.data["is_visible_to_volunteers"]:
            self.send_notification(registration_ids, title, kwargs["pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeedDetails(generics.UpdateAPIView):
    queryset = File.objects.all()
    serializer_class = FeedSerializer
    # permission_classes = (HasFilePermissions, )

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Feed, id=self.kwargs["feed_id"])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "image" in request.data and request.data["image"] is not None and request.data["image"] != "":
            instance.image.delete(save=False)
            image = request.data["image"]
            image = CaseUtils.save_image(image)
            request.data["image"] = image

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)


class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (HasFilePermissions,)

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        queryset = File.objects.filter(case=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # request.data._mutable = True if request.data._mutable else None
        request.data["user"] = request.user.id
        request.data["case"] = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (HasFilePermissions,)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(File, id=self.kwargs["file_id"])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "image" in request.data and request.data["image"] is not None and request.data["image"] != "":
            instance.image.delete(save=False)
            image = request.data["image"]
            image = CaseUtils.save_image(image)
            request.data["image"] = image

        if "file" in request.data and request.data["file"] is not None and request.data["file"] != "":
            instance.file.delete(save=False)
            file = request.data["file"]
            request.data["file"] = file

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.image)))
        if instance.file:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(instance.file)))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadImage(APIView):
    def get(self, request, pk, **kwargs):
        file = get_object_or_404(File, id=kwargs.get("file_id", None))
        data = str(file.image).split(".")
        file_format = data[len(data) - 1]
        file_format = "jpeg" if file_format == "jpg" else file_format
        image = Image.open(file.image)
        response = HttpResponse(content_type="image/*")
        image.save(response, file_format)
        return response


class DownloadFile(APIView):
    def get(self, request, pk, **kwargs):
        file = get_object_or_404(File, id=kwargs.get("file_id", None))
        with open(os.path.join("media/", str(file.file)), "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/*")
            return response


def save_case(data, serializer, owner=None):
    # social_media_data = data["social_media_data"] if "social_media_data" in data else None
    serializer.is_valid(raise_exception=True)
    # serializer.save(social_media_data=social_media_data, owner=owner)
    serializer.save(owner=owner)


class CaseList(generics.ListCreateAPIView):
    serializer_class = CasesSerializer
    permission_classes = (HasGeneralAdminPermissions, HasCreateCasesPermissions)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        child_id = self.request.query_params.get("child_id", None)
        is_active = self.request.query_params.get("is_active", False)

        if is_active == "true":
            return Case.get_web_queryset(child_id, organization_id).filter(status="active")
        elif is_active == "false":
            return Case.get_web_queryset(child_id, organization_id).filter(status="closed")
        elif is_active == "archived":
            return Case.get_web_queryset(child_id, organization_id).filter(status="archived")
        else:
            return Case.get_web_queryset(child_id, organization_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["full_name"] = "{} {}".format(data["first_name"], data["last_name"])
        if "child_id" in data:
            child_instance = get_object_or_404(Child, id=data["child_id"])
            child_serializer = ChildSerializer(child_instance, data=request.data, partial=True)
            child_serializer.is_valid()
            child_serializer.save()
        else:
            child_serializer = ChildSerializer(data=data)
            child_serializer.is_valid(raise_exception=True)
            child_serializer.save()

        data["child"] = child_serializer.data.get("id")
        if request.user.role == "Facility_manager":
            data["status"] = "inactive"
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        save_case(self.request.data, serializer, self.request.user)


class CaseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CasesSerializer
    permission_classes = (
        HasGeneralAdminPermissions,
        HasCaseOrganizationAdminPermissions,
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        data = request.data
        if "first_name" in data or "last_name" in data:
            data["full_name"] = "{} {}".format(data["first_name"], data["last_name"])

        if (
            "profile_photo" in request.data
            and request.data["profile_photo"] is not None
            and request.data["profile_photo"] != ""
        ):
            instance.profile_photo.delete(save=False)
            profile_photo = request.data["profile_photo"]
            image = CaseUtils.save_image(profile_photo)
            request.data["profile_photo"] = image
        else:
            child_serializer = ChildSerializer(instance.child, data=request.data, partial=partial)
            child_serializer.is_valid()
            self.perform_update(child_serializer)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        save_case(self.request.data, serializer)


class SocialMediaList(generics.ListCreateAPIView):
    serializer_class = SocialMediaSerializer
    # permission_classes = (HasGeneralAdminPermissions, HasCreateCasesPermissions)

    def get_queryset(self):
        case_id = self.request.query_params.get("case_id", None)
        organization_id = self.request.user.organization_id
        case = get_object_or_404(Case, id=case_id)
        if organization_id != case.organization.id:
            raise Exception
        return SocialMedia.objects.filter(case=case)


class SocialMediaDetails(generics.RetrieveUpdateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = (permissions.IsAuthenticated,)


class AddCaseVolunteer(APIView):
    @staticmethod
    def send_notification(registration_ids, data):
        data_message = {
            "type": "volunteer_invite_notification",
            "title": data,
        }
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        try:
            push_service.notify_multiple_devices(
                registration_ids=registration_ids,
                # message_title=title,
                # message_body=description,
                data_message=data_message,
                android_channel_id="cr",
                # sound='Default',
                # badge=1
            )
        except Exception as exception:
            print(exception)

    def post(self, request, *args, **kwargs):
        user_ids = request.data["userIds"]
        message = request.data["message"]
        case_id = kwargs["pk"]
        case = get_object_or_404(Case, id=case_id)
        for user_id in user_ids:
            exists = len(CaseVolunteer.objects.filter(case=case, user=get_object_or_404(User, id=user_id))) > 0
            if not exists:
                uuids = Uuid.objects.filter(user=user_id)
                if len(uuids) <= 0:
                    return Response("Account not activated yet!", status=status.HTTP_204_NO_CONTENT)
                devices = FCMDevice.objects.filter(uuid__in=uuids)
                registration_ids = []
                for device in devices:
                    registration_ids.append(device.registration_id)
                if len(registration_ids) <= 0:
                    return Response("Account's firebase token not exists!", status=status.HTTP_204_NO_CONTENT)
                CaseVolunteer.objects.create(case=case, user=get_object_or_404(User, id=user_id))
                title = "You have been invited to participate as a volunteer for case: {}".format(case.custom_name)
                title += message
                print(title)
                self.send_notification(registration_ids, title)
        return Response("Case volunteers added!", status=status.HTTP_200_OK)


class CaseVolunteerList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CaseVolunteerSerializer

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        # self.check_object_permissions(self.request, get_object_or_404(Case, id=pk))
        queryset = CaseVolunteer.objects.filter(case=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CaseVolunteerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CaseVolunteerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        volunteer = get_object_or_404(CaseVolunteer, id=self.kwargs["volunteer_id"])
        return volunteer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "password" in request.data:
            request.data.pop("password")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class FacilityCaseList(generics.ListAPIView):
    serializer_class = CasesSerializer
    permission_classes = (HasGeneralAdminPermissions, HasCreateCasesPermissions)

    def get_queryset(self):
        cases_ids = FacilityHistory.objects.values_list("case_id", flat=True).filter(
            facility=self.request.user.facility_id, is_active=True
        )

        case_status = self.request.query_params.get("status", None)
        if case_status is not None and case_status == "active":
            return Case.objects.filter(pk__in=cases_ids, status=case_status).order_by("-arrival_at_facility_date")[:8]

        presence_status = self.request.query_params.get("presence_status", None)
        if presence_status is not None:
            return Case.objects.filter(pk__in=cases_ids, presence_status=presence_status).order_by(
                "-arrival_at_facility_date"
            )[:8]

        return Case.objects.filter(pk__in=cases_ids).order_by("-arrival_at_facility_date")[:8]


class FacilityCaseDetails(CaseDetails):
    permission_classes = (permissions.IsAuthenticated,)


class FacilityCaseState(APIView):
    permission_classes = (HasGeneralAdminPermissions, FacilityCaseStatePermissions)

    @staticmethod
    def get(request, *args, **kwargs):
        presence_status = request.query_params.get("presence_status", None)
        case = get_object_or_404(Case, pk=kwargs["pk"])
        if presence_status == "transit":
            facility_history_object = FacilityHistory.objects.get(case=case, is_active=True)
            facility_history_object.is_active = False
            facility_history_object.date_left = datetime.datetime.now(get_localzone())
            facility_history_object.save()
        case.presence_status = presence_status
        case.save()
        return Response("Case presence_status field is updated!".format(case.id), status=status.HTTP_200_OK,)


class FacilityCaseReportMissing(APIView):
    permission_classes = (HasGeneralAdminPermissions,)

    @staticmethod
    def get(request, *args, **kwargs):
        case = get_object_or_404(Case, pk=kwargs["pk"])
        case.status = "active"
        case.presence_status = "missing"
        case.save()
        facility_history_object = FacilityHistory.objects.get(case=case, is_active=True)
        facility_history_object.is_active = False
        facility_history_object.date_left = datetime.datetime.now(get_localzone())
        facility_history_object.save()
        return Response("Case status is: active!", status=status.HTTP_200_OK)


class CloseCase(APIView):
    permission_classes = (
        HasCaseManagerPermissions,
        HasCaseOrganizationAdminPermissions,
        HasCloseCasePermissions,
    )

    @staticmethod
    def send_notification(case):
        data_message = {
            "type": "close_case_notification",
            "title": case.custom_name,
        }
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        followers = Follower.objects.filter(case=case.id, is_active=True).values_list("user", flat=True)
        followers_uuid = Uuid.objects.filter(user__in=followers)
        devices = FCMDevice.objects.filter(uuid__in=followers_uuid)
        registration_ids = []
        for device in devices:
            if device is not None and device.active is True:
                registration_ids.append(device.registration_id)
        try:
            push_service.notify_multiple_devices(
                registration_ids=registration_ids,
                # message_title=title,
                # message_body=description,
                data_message=data_message,
                android_channel_id="cr",
                # sound='Default',
                # badge=1
            )
        except Exception as exception:
            print(exception)

    # @staticmethod
    def get(self, request, *args, **kwargs):
        case_id = kwargs.pop("pk", None)
        local_now = datetime.datetime.now(get_localzone())
        case = Case.objects.get(pk=case_id)
        if case.status == "active":
            Alert.objects.filter(case_id=case_id, is_active=True).update(is_active=False)
            case.status = "closed"
            case.end_date = local_now
            case.save()
            self.send_notification(case)
        followers = Follower.objects.filter(case=case_id)
        for follower in followers:
            follower.is_active = False
            follower.save()
        changeStatus(case.blockchain_address, case.status)
        return Response("Case {} closed".format(case_id), status=status.HTTP_200_OK)


class ArchiveCase(APIView):
    permission_classes = (
        HasCaseManagerPermissions,
        HasCaseOrganizationAdminPermissions,
        HasArchiveCasePermissions,
    )

    def get(self, request, *args, **kwargs):
        case_id = kwargs.pop("pk", None)
        local_now = datetime.datetime.now(get_localzone())
        case = Case.objects.get(pk=case_id)
        case.status = "archived"
        case.save()

        # if the child was living in facility, change is_present/date_left in facility
        # FacilityHistory.objects.filter(case_id=case_id, is_active=True).update(is_active=False, date_left=local_now)

        return Response("Case {} archived".format(case_id), status=status.HTTP_200_OK)
