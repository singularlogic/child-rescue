from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from organizations.utils import OrganizationUtils

from organizations.models import Organization
from users.models import User

from users.web_admin_api.serializers import UserSerializer
from .serializers import OrganizationSerializer, OrganizationUsersSerializer

from organizations.web_admin_api.permissions import (
    OrganizationPermissions,
    OrganizationObjectPermissions,
    CreateUserPermissions,
)


class OtherOrganizationList(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    # permission_classes = (OrganizationPermissions,)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        return Organization.objects.exclude(id=organization_id)


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    # permission_classes = (OrganizationPermissions,)


class OrganizationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (OrganizationObjectPermissions,)

    def update(self, request, *args, **kwargs):
        print(request.data)
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if (
            "logo" in request.data
            and request.data["logo"] is not None
            and request.data["logo"] != ""
        ):
            instance.logo.delete(save=False)
            logo = request.data["logo"]
            image = OrganizationUtils.save_image(logo)
            request.data["logo"] = image

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            print(e)
        return Response(serializer.data)


class OrganizationUsersCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (CreateUserPermissions,)

    def create(self, request, *args, **kwargs):
        self.check_object_permissions(
            self.request, request.data.get("organization", None)
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class OrganizationUsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizationUsersSerializer
    permission_classes = (OrganizationObjectPermissions,)

    def list(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        user_id = request.query_params.get("user_id", None)
        role = request.query_params.get("role", None)
        self.check_object_permissions(
            self.request, get_object_or_404(Organization, id=pk)
        )
        queryset = Organization.objects.get_organization_users(pk, user_id, role)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OrganizationUserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizationUsersSerializer
    permission_classes = (OrganizationObjectPermissions,)

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        user_id = self.request.query_params.get("user_id", None)
        if user_id is not None:
            self.check_object_permissions(
                self.request, get_object_or_404(Organization, id=pk)
            )
            return Organization.objects.get_organization_users(pk, user_id).first()
        raise Exception("You must provide user_id")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()

        if "password" in request.data:
            request.data.pop("password")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
