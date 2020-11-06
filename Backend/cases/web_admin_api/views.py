import os
import json
import datetime
import requests

from PIL import Image
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from alerts.models import Alert
from analytics.analytics_basic import IntelliSearch
import analytics.analytics_case as ac

# from blockchain.blockchain import changeStatus
from cases.models import (
    FacilityHistory,
    Case,
    Follower,
    CaseVolunteer,
    File,
    Feed,
    Child,
    SocialMedia,
    AnonymizedCase,
    SharedCase, LinkedCase,
)
from feedbacks.models import Feedback

from cases.utils import CaseUtils
from cases.web_admin_api.permissions import (
    FacilityCaseStatePermissions,
    HasOrganizationPermissions,
    HasCloseCasePermissions,
    HasArchiveCasePermissions,
    HasFilesOrganizationPermissions,
)
from firebase.models import FCMDevice
from firebase.pyfcm import FCMNotification
from organizations.models import Organization
from places.models import Place
from users.models import Uuid, User
from users.web_admin_api.permissions import (
    HasGeneralAdminPermissions,
    HasCaseManagerPermissions,
    HasNetworkManagerPermissions,
)
from .serializers import (
    # CaseSerializer,
    CasesSerializer,
    SimilarCasesSerializer,
    CaseVolunteerSerializer,
    FileSerializer,
    FeedSerializer,
    ChildSerializer,
    SocialMediaSerializer,
    AnonymizedCaseSerializer,
    ArchivedCaseSerializer,
    SharedCasesSerializer, LinkedCasesSerializer,
)
from tzlocal import get_localzone


class ActiveVolunteerList(APIView):
    permission_classes = (HasCaseManagerPermissions,)

    def get(self, request, *args, **kwargs):
        queryset = CaseVolunteer.objects.filter(has_accept_invitation=True, case__status="active")
        return Response(len(queryset))


class NumberOfPlacesList(APIView):
    permission_classes = (HasCaseManagerPermissions,)

    def get(self, request, *args, **kwargs):
        queryset = Place.objects.filter(case__status="active")
        return Response(len(queryset))


class SimilarCasesList(generics.ListCreateAPIView):
    permission_classes = (HasCaseManagerPermissions,)
    serializer_class = SimilarCasesSerializer

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        case = get_object_or_404(Case, pk=pk)
        ceng = ac.ProfileEvalEngine(case)
        p_json1 = ceng.get_profiling_preds_json()  # compute_probability and return json
        similar_list = ceng.fetch_similar_closed_cases(
            request.user.organization, 5
        )  # return list of 2 similar cases ids
        queryset = Case.objects.select_related("child").filter(id__in=similar_list)[:4]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LinkedCasesList(generics.ListCreateAPIView):
    permission_classes = (HasCaseManagerPermissions,)
    serializer_class = LinkedCasesSerializer

    def list(self, request, *args, **kwargs):
        linked_cases = []
        pk = kwargs.get("pk", None)
        case = get_object_or_404(Case, pk=pk)
        queryset = LinkedCase.objects.filter(case=case)
        for case_object in queryset:
            linked_cases.append(case_object.linked_case)

        queryset = LinkedCase.objects.filter(linked_case=case)
        for case_object in queryset:
            linked_cases.append(case_object.case)

        serializer = self.get_serializer(linked_cases, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        case = get_object_or_404(Case, pk=pk)
        linked_case = get_object_or_404(Case, id=request.data["case_id"])
        new_linked_case = LinkedCase.objects.create(case=case, linked_case=linked_case)
        new_linked_case.save()
        return Response(status=status.HTTP_201_CREATED)


class LinkedCaseDetails(generics.DestroyAPIView):
    queryset = LinkedCase.objects.all()
    serializer_class = FeedSerializer
    permission_classes = (HasOrganizationPermissions, )

    # def get_object(self, *args, **kwargs):
    #     return get_object_or_404(LinkedCase, case=self.kwargs["pk"], linked_case=self.kwargs["linked_case_id"])

    def destroy(self, request, *args, **kwargs):
        instance = LinkedCase.objects.filter(case=self.kwargs["pk"], linked_case=self.kwargs["linked_case_id"])
        if len(instance) == 0:
            instance = LinkedCase.objects.filter(case=self.kwargs["linked_case_id"], linked_case=self.kwargs["pk"])
        self.perform_destroy(instance[0])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChildrenList(APIView):
    permission_classes = (HasCaseManagerPermissions,)

    def get(self, request, **kwargs):
        name = request.query_params.get("name", None)
        case_id = request.query_params.get("case_id", None)
        queryset = IntelliSearch().run_rawsql_namesearch(name, request.user.organization_id)
        formatted_response = list()

        if case_id is not None:
            current_case = Case.objects.get(id=case_id)

        for child in queryset:
            if case_id is not None and str(child[3]) == str(case_id):
                continue

            anonymized_case = AnonymizedCase.objects.filter(case_id=child[3]).first()
            case = Case.objects.get(id=child[3])

            is_linked_case = LinkedCase.objects.filter(Q(case=current_case, linked_case=case) | Q(case=case, linked_case=current_case)).count() > 0 if case_id is not None else False
            image = None
            if case.profile_photo:
                image = request.build_absolute_uri(settings.BASE_URL + case.profile_photo.url)
            if anonymized_case is not None:
                formatted_response.append(
                    {
                        "id": child[0],
                        "first_name": anonymized_case.first_name,
                        "last_name": anonymized_case.last_name,
                        "case_id": child[3],
                        "status": child[4],
                        "rank": child[5],
                        "image": image,
                        "is_linked": is_linked_case
                    }
                )
            else:
                formatted_response.append(
                    {
                        "id": child[0],
                        "first_name": child[1],
                        "last_name": child[2],
                        "case_id": child[3],
                        "status": child[4],
                        "rank": child[5],
                        "image": image,
                        "is_linked": is_linked_case
                    }
                )

        return Response(formatted_response)


class ChildDetails(generics.RetrieveAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = (HasCaseManagerPermissions,)


class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = (HasOrganizationPermissions, HasGeneralAdminPermissions)

    @staticmethod
    def send_notification(registration_ids, title, case_id, custom_name):
        data_message = {"type": "post_notification", "title": title, "case_id": case_id, "case_name": custom_name}
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
        queryset = Feed.objects.filter(case=pk).order_by("-id")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # if not request.data._mutable:
        #     request.data._mutable = True
        # print("XOXOXO")
        # print(request.data)
        # print(request.data['radius'])
        # print(request.data['selected_volunteers'])
        report = []
        request.data["user"] = request.user.id
        request.data["case"] = kwargs.get("pk")
        case = get_object_or_404(Case, id=kwargs["pk"])
        registration_ids = []
        case_volunteers = []
        if request.data["is_visible_to_volunteers"]:
            case_volunteers = CaseVolunteer.objects.filter(case=case, has_accept_invitation=True)

        if (
            "selected_volunteers" in request.data
            and request.data["selected_volunteers"]
            and len(request.data["selected_volunteers"]) > 0
        ):
            user_ids = []
            for item in request.data["selected_volunteers"]:
                user_ids.append(item["user"])
            case_volunteers = CaseVolunteer.objects.filter(case=case, user__in=user_ids)

        for case_volunteer in case_volunteers:
            user_report = {}
            uuids = Uuid.objects.filter(user=case_volunteer.user)
            if len(uuids) <= 0:
                # return Response("Account not activated yet!", status=status.HTTP_204_NO_CONTENT)
                user_report["user"] = case_volunteer.user
            devices = FCMDevice.objects.filter(uuid__in=uuids)
            for device in devices:
                registration_ids.append(device.registration_id)
            if len(registration_ids) <= 0:
                user_report["devices"] = devices
                # return Response("Account's firebase token not exists!", status=status.HTTP_204_NO_CONTENT)
            report.append(user_report)
        print("Report for notifications in feed.")
        print(report)
        title = "New post for case: {}".format(case.custom_name)
        self.send_notification(registration_ids, title, kwargs["pk"], case.custom_name)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeedDetails(generics.UpdateAPIView):
    queryset = File.objects.all()
    serializer_class = FeedSerializer
    permission_classes = (HasOrganizationPermissions, HasGeneralAdminPermissions)

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
    permission_classes = (HasFilesOrganizationPermissions, HasGeneralAdminPermissions)

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
    permission_classes = (HasFilesOrganizationPermissions, HasGeneralAdminPermissions)

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
    permission_classes = (HasOrganizationPermissions, HasGeneralAdminPermissions)

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
    permission_classes = (HasOrganizationPermissions, HasGeneralAdminPermissions)

    def get(self, request, pk, **kwargs):
        file = get_object_or_404(File, id=kwargs.get("file_id", None))
        with open(os.path.join(settings.MEDIA_ROOT, str(file.file)), "rb") as fh:
            response = HttpResponse(fh.read(), content_type="application/*")
            return response


def save_case(data, serializer, owner=None):
    # social_media_data = data["social_media_data"] if "social_media_data" in data else None
    serializer.is_valid(raise_exception=True)
    # serializer.save(social_media_data=social_media_data, owner=owner)
    serializer.save(owner=owner)


class SharedOrganizationList(generics.ListCreateAPIView):
    serializer_class = SharedCasesSerializer
    # permission_classes = (HasOrganizationPermissions, HasCaseManagerPermissions)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        case_id = self.request.query_params.get("caseId", False)
        return SharedCase.objects.filter(case=case_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        case_id = self.request.query_params.get("caseId", False)
        shared_cases = SharedCase.objects.filter(case=case_id)
        for shared_case in shared_cases:
            shared_case.delete()
        for organization in data["organizations"]:
            if organization["selected"]:
                organization = get_object_or_404(Organization, id=organization["id"])
                case = get_object_or_404(Case, id=case_id)
                SharedCase.objects.create(organization=organization, case=case)
        return Response(status=status.HTTP_201_CREATED)


class DashboardCaseList(generics.ListCreateAPIView):
    serializer_class = CasesSerializer
    permission_classes = (HasOrganizationPermissions, HasCaseManagerPermissions)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        feedbacks = Feedback.objects.filter(
            organization=organization_id, is_main=True, date__gte=start_date, date__lte=end_date
        ).select_related("case")
        cases = list()
        for feedback in feedbacks:
            cases.append(feedback.case)
        return cases


class CaseList(generics.ListCreateAPIView):
    serializer_class = CasesSerializer
    permission_classes = (HasOrganizationPermissions, HasCaseManagerPermissions)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        child_id = self.request.query_params.get("child_id", None)
        is_active = self.request.query_params.get("is_active", False)

        if is_active == "all":
            return Case.get_web_queryset(child_id, organization_id).exclude(status="archived")
        elif is_active == "true":
            return Case.get_web_queryset(child_id, organization_id).filter(status="active")
        elif is_active == "false":
            return Case.get_web_queryset(child_id, organization_id).filter(status="closed")
        elif is_active == "archived":
            return Case.get_web_queryset(child_id, organization_id).filter(status="archived")
        else:
            return Case.get_web_queryset(child_id, organization_id)

    def create(self, request, *args, **kwargs):
        data = request.data
        first_name = data["first_name"] if "first_name" in data else ""
        last_name = data["last_name"] if "last_name" in data else ""
        data["full_name"] = "{} {}".format(first_name, last_name)
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
        HasCaseManagerPermissions,
        HasOrganizationPermissions,
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        data = request.data
        first_name = data["first_name"] if "first_name" in data else ""
        last_name = data["last_name"] if "last_name" in data else ""
        data["full_name"] = "{} {}".format(first_name, last_name)
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
    permission_classes = (
        HasCaseManagerPermissions,
        HasOrganizationPermissions,
    )

    def get_queryset(self):
        case_id = self.request.query_params.get("case_id", None)
        organization_id = self.request.user.organization_id
        case = get_object_or_404(Case, id=case_id)
        shared_case = SharedCase.objects.filter(case=case).first()
        is_shared_case = False
        if shared_case is not None:
            is_shared_case = organization_id == shared_case.organization.id
        if organization_id != case.organization.id and not is_shared_case:
            raise Exception
        return SocialMedia.objects.filter(case=case).order_by("medium")


class SocialMediaDetails(generics.RetrieveUpdateAPIView):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = (
        HasCaseManagerPermissions,
        # HasOrganizationPermissions,
    )

    # def get_object(self, *args, **kwargs):
    #     social_media = get_object_or_404(SocialMedia, id=self.kwargs["pk"])
    #     return social_media
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop("partial", True)
    #     instance = self.get_object()
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class AddCaseVolunteer(APIView):
    permission_classes = (HasOrganizationPermissions, HasNetworkManagerPermissions)

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
                    return Response("Account's firebase token not exists!", status=status.HTTP_204_NO_CONTENT,)
                CaseVolunteer.objects.create(case=case, user=get_object_or_404(User, id=user_id))
                title = "You have been invited to participate as a volunteer for case: {}".format(case.custom_name)
                title += message
                print(title)
                self.send_notification(registration_ids, title)
        return Response("Case volunteers added!", status=status.HTTP_200_OK)


class CaseVolunteerList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CaseVolunteerSerializer
    permission_classes = (HasOrganizationPermissions, HasNetworkManagerPermissions)

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
    permission_classes = (HasOrganizationPermissions, HasNetworkManagerPermissions)

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
    permission_classes = (HasOrganizationPermissions,)

    def get_queryset(self):
        cases_ids = FacilityHistory.objects.values_list("case_id", flat=True).filter(
            facility=self.request.user.facility_id, is_active=True
        )

        case_status = self.request.query_params.get("status", None)
        if case_status is not None and case_status == "active":
            return Case.objects.filter(pk__in=cases_ids, status=case_status).order_by("-arrival_at_facility_date")

        presence_status = self.request.query_params.get("presence_status", None)
        if presence_status is not None:
            return Case.objects.filter(pk__in=cases_ids, presence_status=presence_status).order_by(
                "-arrival_at_facility_date"
            )

        return Case.objects.filter(pk__in=cases_ids).order_by("-arrival_at_facility_date")


class FacilityCaseDetails(CaseDetails):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (HasOrganizationPermissions,)


class FacilityCaseState(APIView):
    # permission_classes = (HasGeneralAdminPermissions, FacilityCaseStatePermissions)
    permission_classes = (HasOrganizationPermissions,)

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
    permission_classes = (HasOrganizationPermissions,)

    @staticmethod
    def post(request, *args, **kwargs):
        case = get_object_or_404(Case, pk=kwargs["pk"])
        case.status = "active"
        case.presence_status = "missing"

        ceng = ac.ProfileEvalEngine(case)
        data = ceng.get_profiling_preds_json()
        case.data = data

        case.has_mobile_phone = request.data.get("has_mobile_phone", None)
        case.has_money_or_credit = request.data.get("has_money_or_credit", None)
        case.has_area_knowledge = request.data.get("has_area_knowledge", None)
        case.clothing_with_scent = request.data.get("clothing_with_scent", None)
        case.is_first_time_missing = request.data.get("is_first_time_missing", None)
        case.transit_country = request.data.get("transit_country", None)

        case.save()
        facility_history_object = FacilityHistory.objects.get(case=case, is_active=True)
        facility_history_object.is_active = False
        facility_history_object.date_left = datetime.datetime.now(get_localzone())
        facility_history_object.save()
        return Response("Case status is: active!", status=status.HTTP_200_OK)


class CloseCase(APIView):
    permission_classes = (
        HasCaseManagerPermissions,
        HasOrganizationPermissions,
        HasCloseCasePermissions,
    )

    @staticmethod
    def send_notification(case, message):
        message = "{case_name}: {case_message}".format(case_name=case.custom_name, case_message=message)
        data_message = {
            "type": "close_case_notification",
            "title": message if message is not None else case.custom_name,
            "case_id": case.id,
        }
        push_service = FCMNotification(api_key=settings.FIREBASE_API_KEY)
        followers = Follower.objects.filter(case=case.id, is_active=True).values_list("user", flat=True)
        followers_uuid = Uuid.objects.filter(user__in=followers)
        devices = FCMDevice.objects.filter(uuid__in=followers_uuid)
        android_registration_ids = []
        ios_registration_ids = []
        for device in devices:
            if device is not None and device.active is True:
                if device.type == "ios_gr" or device.type == "ios_be":
                    ios_registration_ids.append(device.registration_id)
                else:
                    android_registration_ids.append(device.registration_id)
        try:
            # push_service.notify_multiple_devices(
            #     registration_ids=ios_registration_ids,
            #     # message_title=data_message["title"],
            #     # message_body=description,
            #     data_message=data_message,
            #     content_available=True,
            #     # sound='Default',
            #     # badge=1
            # )

            print("GO2")
            url = "https://us-central1-childrescue-f8c82.cloudfunctions.net/setIosNotification"
            login_request = requests.post(url, data=data_message)
            response = login_request.json()
            print(response)
            print("OK2")

            push_service.notify_multiple_devices(
                registration_ids=android_registration_ids,
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
    def post(self, request, *args, **kwargs):
        import dateutil.parser

        message = (
            request.data["message"]
            if "message" in request.data and request.data["message"] is not None and len(request.data["message"]) > 0
            else None
        )

        case_id = kwargs.pop("pk", None)
        local_now = datetime.datetime.now(get_localzone())

        first_feedback_date = Feedback.objects.filter(case=case_id).first().date
        # first_feedback_date = datetime.datetime.fromisoformat(str(first_feedback_date))
        first_feedback_date = dateutil.parser.isoparse(str(first_feedback_date))
        last_feedback_date = Feedback.objects.filter(case=case_id).last().date
        # last_feedback_date = datetime.datetime.fromisoformat(str(last_feedback_date))
        last_feedback_date = dateutil.parser.isoparse(str(last_feedback_date))
        diff = last_feedback_date - first_feedback_date
        hours_diff = divmod(diff.seconds, 3600)[0]
        days = hours_diff / 24

        case = Case.objects.get(pk=case_id)
        if case.status == "active":
            Alert.objects.filter(case_id=case_id, is_active=True).update(is_active=False)
            case.status = "closed"
            case.end_date = local_now
            case.days_diff = days
            case.save()
            self.send_notification(case, message)

        shared_cases = SharedCase.objects.filter(case=case_id)
        for shared_case in shared_cases:
            shared_case.delete()
        # followers = Follower.objects.filter(case=case_id)
        # for follower in followers:
        #     follower.is_active = False
        #     follower.save()
        # blockchain_integration
        # changeStatus(case.blockchain_address, case.status)
        return Response("Case {} closed".format(case_id), status=status.HTTP_200_OK)


class DeactivateAlerts(APIView):
    permission_classes = (
        HasCaseManagerPermissions,
        HasOrganizationPermissions,
        HasCloseCasePermissions,
    )

    def post(self, request, *args, **kwargs):
        case_id = kwargs.pop("pk", None)
        case = Case.objects.get(pk=case_id)
        if case.status == "active":
            Alert.objects.filter(case_id=case_id, is_active=True).update(is_active=False)
        return Response("Case {} alerts, deactivated.".format(case_id), status=status.HTTP_200_OK)


class ArchiveCase(APIView):
    # serializer_class = ArchivedCaseSerializer
    permission_classes = (
        HasCaseManagerPermissions,
        HasOrganizationPermissions,
        HasArchiveCasePermissions,
    )

    def get(self, request, *args, **kwargs):
        case_id = kwargs.pop("pk", None)
        # local_now = datetime.datetime.now(get_localzone())
        case = Case.objects.get(pk=case_id)
        case.status = "archived"
        case.save()

        data = ArchivedCaseSerializer(case).data
        data = json.dumps(data, ensure_ascii=False).encode("utf8")
        data = data.decode()
        # print(a.decode())

        import requests

        server = os.getenv("UBI_SERVER")
        endpoint = "{}/newCase".format(server)
        r = requests.post(
            endpoint,
            headers={"accept": "json / application", "Content-Type": "application/json",},
            data=data,
            verify=False,
        )
        print(r.status_code)
        # response = r.json()
        # print(response)

        # if the child was living in facility, change is_present/date_left in facility
        # FacilityHistory.objects.filter(case_id=case_id, is_active=True).update(is_active=False, date_left=local_now)

        return Response("Case {} archived".format(case_id), status=status.HTTP_200_OK)


class AnonymizedCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnonymizedCase.objects.all()
    serializer_class = AnonymizedCaseSerializer
    permission_classes = (HasOrganizationPermissions,)

    def get_object(self, *args, **kwargs):
        return get_object_or_404(AnonymizedCase, case_id=self.kwargs["pk"])


class AnonymizedCaseList(generics.ListAPIView):
    serializer_class = AnonymizedCaseSerializer
    permission_classes = (HasOrganizationPermissions,)

    def get_queryset(self):
        import requests

        server = os.getenv("UBI_SERVER")
        endpoint = "{}/getData".format(server)
        r = requests.get(endpoint, headers={"Content-Type": "application/json",}, verify=False,)
        response = r.json()
        for case in response:
            _, created = AnonymizedCase.objects.update_or_create(
                case_id=case["id"],
                defaults={
                    "disappearance_date": case["disappearance_date"],
                    "disappearance_location": case["disappearance_location"],
                    # "arrival_date": case["arrival_date"],
                    "first_name": case["first_name"],
                    "last_name": case["last_name"],
                    # "father_fullname": case["father_fullname"],
                    # "mother_fullname": case["mother_fullname"],
                    # "gender": case["gender"],
                    # "phone": case["phone"],
                    "date_of_birth": case["date_of_birth"],
                    "organization": int(case["organization"]) if case["organization"] else None,
                    # "custom_name": case["custom_name"],
                    # "presence_status": case["presence_status"],
                    # "status": case["status"],
                    # "arrival_at_facility_date": case["arrival_at_facility_date"],
                    # "end_date": case["end_date"],
                    # "description": case["description"],
                    # "has_mobile_phone": case["has_mobile_phone"],
                    # "has_money_or_credit": case["has_money_or_credit"],
                    # "has_area_knowledge": case["has_area_knowledge"],
                    # "clothing_with_scent": case["clothing_with_scent"],
                    # "rescue_teams_utilized": case["rescue_teams_utilized"],
                    # "volunteers_utilized": case["volunteers_utilized"],
                    # "transit_country": case["transit_country"],
                    "disappearance_type": case["disappearance_type"],
                    "amber_alert": case["amber_alert"],
                    # "eye_color": case["eye_color"],
                    # "hair_color": case["hair_color"],
                    # "skin_color": case["skin_color"],
                    # "height": case["height"],
                    # "weight": case["weight"],
                    # "stature": case["stature"],
                    # "body_type": case["body_type"],
                    # "haircut": case["haircut"],
                    # "characteristics": case["characteristics"],
                    # "home_address": case["home_address"],
                    # "home_country": case["home_country"],
                    # "home_postal_code": case["home_postal_code"],
                    # "birth_country": case["birth_country"],
                    # "education_level": case["education_level"],
                    # "languages_spoken": case["languages_spoken"],
                    "nationality": case["nationality"],
                    # "addiction": case["addiction"],
                    # "health_issues": case["health_issues"],
                    # "medical_treatment_required": case["medical_treatment_required"],
                    # "health_issues_description": case["health_issues_description"],
                    # "triggered_event": case["triggered_event"],
                    # "concerns": case["concerns"],
                    # "mental_disorders": case["mental_disorders"],
                    # "psychological_disorders": case["psychological_disorders"],
                    # "physical_disabilities": case["physical_disabilities"],
                    # "living_environment": case["living_environment"],
                    # "family_members": case["family_members"],
                    # "school_grades": case["school_grades"],
                    # "hobbies": case["hobbies"],
                    # "relationship_status": case["relationship_status"],
                    # "religion": case["religion"],
                    # "disappearance_reasons": case["disappearance_reasons"],
                    # "parents_profile": case["parents_profile"],
                    # "is_high_risk": case["is_high_risk"],
                    # "is_first_time_missing": case["is_first_time_missing"],
                    # "has_trafficking_history": case["has_trafficking_history"],
                    # "is_refugee": case["is_refugee"],
                    # "legal_status": case["legal_status"],
                    # "contacted_date": case["contacted_date"],
                    # "risk_indicator": case["risk_indicator"],
                    # "days_diff": case["days_diff"],
                    # "go_missing_possibility": case["go_missing_possibility"],
                    # "current_mindset": case["current_mindset"],
                },
            )
        cases = AnonymizedCase.objects.filter(organization=str(self.request.user.organization.id))
        return cases
