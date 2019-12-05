from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cases.mobile_api.permissions import HasVolunteerPermissions
from cases.models import Case, Follower, CaseVolunteer, CaseVolunteerLocation, Feed
from .serializers import (
    CaseSerializer,
    FollowerSerializer,
    CaseVolunteerSerializer,
    CaseVolunteerLocationSerializer,
    FeedSerializer,
)


class CaseList(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class CaseDetails(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class FollowedCases(generics.ListAPIView):
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        followed_cases_records = Follower.objects.filter(user=self.request.user.id)
        followed_cases = []
        for item in followed_cases_records:
            if item.is_active:
                followed_cases.append(Case.objects.get(id=item.case.id))
        return followed_cases


class FollowCase(APIView):
    serializer_class = FollowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        case = self.get_object(pk)
        followed_case, created = Follower.objects.get_or_create(case=case, user=request.user)

        if created or not followed_case.is_active:
            followed_case.is_active = True
            followed_case.save()

        return Response(self.serializer_class(followed_case).data, status=status.HTTP_200_OK)


class UnfollowCase(APIView):
    serializer_class = FollowerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Case.objects.get(pk=pk)
        except Case.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        case = self.get_object(pk)
        followed_case = Follower.objects.get(case=case, user=request.user)

        if followed_case is not None and followed_case.is_active:
            followed_case.is_active = False
            followed_case.save()

        return Response(self.serializer_class(followed_case).data, status=status.HTTP_200_OK)


class VolunteerCasesList(generics.ListAPIView):
    queryset = CaseVolunteer.objects.all()
    serializer_class = CaseVolunteerSerializer
    permission_classes = (permissions.IsAuthenticated, HasVolunteerPermissions)

    def list(self, request, *args, **kwargs):
        has_accept_invitation = request.query_params.get("has_accept_invitation", None)
        if has_accept_invitation == "all":
            queryset = CaseVolunteer.objects.filter(user=request.user)
        else:
            queryset = CaseVolunteer.objects.filter(user=request.user, has_accept_invitation=has_accept_invitation)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AcceptInvite(APIView):
    serializer_class = CaseVolunteerSerializer
    permission_classes = (permissions.IsAuthenticated, HasVolunteerPermissions)

    def post(self, request, **kwargs):
        case_volunteer = get_object_or_404(CaseVolunteer, case=kwargs.get("pk", None), user=request.user)
        case_volunteer.has_accept_invitation = True
        case_volunteer.save()
        return Response(self.serializer_class(case_volunteer).data, status=status.HTTP_200_OK)


class DeclineInvite(APIView):
    serializer_class = CaseVolunteerSerializer
    permission_classes = (permissions.IsAuthenticated, HasVolunteerPermissions)

    def post(self, request, **kwargs):
        case_volunteer = get_object_or_404(CaseVolunteer, case=kwargs.get("pk", None), user=request.user)
        case_volunteer.has_accept_invitation = False
        case_volunteer.save()
        return Response(self.serializer_class(case_volunteer).data, status=status.HTTP_200_OK)


class VolunteerCasesLocation(generics.CreateAPIView):
    queryset = CaseVolunteerLocation.objects.all()
    serializer_class = CaseVolunteerLocationSerializer
    permission_classes = (permissions.IsAuthenticated, HasVolunteerPermissions)

    def create(self, request, *args, **kwargs):
        case_id = self.kwargs.get("pk", None)
        case_volunteer = get_object_or_404(CaseVolunteer, user=self.request.user, case=case_id)
        self.request.data["case_volunteer"] = case_volunteer.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FeedList(generics.ListCreateAPIView):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        HasVolunteerPermissions,
    )

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        queryset = Feed.objects.filter(case=pk, is_visible_to_volunteers=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True
        request.data["user"] = request.user.id
        request.data["case"] = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
