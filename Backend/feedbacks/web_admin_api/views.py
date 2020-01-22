import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.analytics_basic import UserRanking
from cases.models import Case
from feedbacks.models import Feedback
from feedbacks.web_admin_api.permissions import (
    HasFeedbackOrganizationAdminPermissions,
    HasUpdateDeleteFeedbackPermissions,
    HasCreateFeedbackPermissions,
    HasGetFeedbackPermissions,
)
from organizations.models import Organization
from users.web_admin_api.permissions import HasGeneralAdminPermissions
from .serializers import FeedbackSerializer
from analytics.web_admin_api.serializers import CountSerializer
from tzlocal import get_localzone


class LatestFeedbackList(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = (HasGeneralAdminPermissions,)

    def get_queryset(self):
        return Feedback.objects.get_latest_web_queryset(self.request.user.organization_id)


class FeedbackList(generics.ListCreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = (HasGeneralAdminPermissions, HasCreateFeedbackPermissions, HasGetFeedbackPermissions)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        case_id = self.request.query_params.get("caseId", None)
        is_superuser = organization_id is None
        if is_superuser:
            organization_id = self.request.query_params.get("organization_id", None)
        return Feedback.objects.get_web_query_set(organization_id, case_id, is_superuser)

    def perform_create(self, serializer):
        organization = Organization.objects.get(id=self.request.user.organization_id)
        case_id = self.request.data["case"]

        if self.request.data["feedback_status"] != "pending":
            checked_by_id = self.request.user.id
            checked_on = datetime.datetime.now(get_localzone())
            serializer.save(
                case=Case.objects.get(id=case_id),
                user=self.request.user,
                checked_by_id=checked_by_id,
                checked_on=checked_on,
                organization=organization,
            )
        else:
            serializer.save(case=Case.objects.get(id=case_id), user=self.request.user, organization=organization)


class FeedbackCountList(APIView):
    permission_classes = (HasGeneralAdminPermissions, HasGetFeedbackPermissions)

    def get(self, request, format=None):
        case_id = self.request.query_params.get("caseId", None)
        group_by = self.request.query_params.get("groupBy", None)
        counts = Feedback.objects.get_feedback_count(case_id, group_by)
        serializer = CountSerializer(counts)
        return Response(serializer.data)


class FeedbackDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (
        HasGeneralAdminPermissions,
        HasUpdateDeleteFeedbackPermissions,
        # HasFeedbackOrganizationAdminPermissions
    )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        del request.data["feedback_image"]
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid()
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user.role in ["volunteer", "simple_user"] and (
            self.request.data["feedback_status"] == "spam" or self.request.data["is_valid"] is not None
        ):
            r = UserRanking(instance.user)
            fr = r.get_new_user_rank()
            instance.user.ranking = fr
            instance.user.save()
        if (
            instance.feedback_status is None
            or (instance.feedback_status == "pending")
            and self.request.data["feedback_status"] != "pending"
        ):
            checked_by_id = self.request.user.id
            checked_on = datetime.datetime.now(get_localzone())
            serializer.save(checked_by_id=checked_by_id, checked_on=checked_on)
        else:
            serializer.save()
