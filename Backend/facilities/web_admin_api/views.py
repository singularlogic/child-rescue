import datetime

from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, status
from django.http.response import JsonResponse

from rest_framework.response import Response

from facilities.models import Facility
from facilities.web_admin_api.permissions import (
    HasAddChildToFacilityPermissions,
    HasFacilityPermissions,
    HasRemoveChildToFacilityPermissions,
)
from users.models import User
from cases.models import Case, FacilityHistory
from users.web_admin_api.permissions import HasGeneralAdminPermissions
from .serializers import FacilitySerializer
from rest_framework.views import APIView
from django.db.models import Q
from facilities.utils import FacilityUtils

from tzlocal import get_localzone


class FacilityList(generics.ListCreateAPIView):
    serializer_class = FacilitySerializer
    permission_classes = (HasFacilityPermissions,)

    def get_queryset(self):
        is_hosting = self.request.query_params.get("is_hosting", None)
        if self.request.user.role == "admin":
            organization_id = self.request.query_params.get("organization_id", None)
        else:
            organization_id = self.request.user.organization_id
        return Facility.objects.get_web_queryset(organization_id, is_hosting)


class FacilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = (HasFacilityPermissions,)


def get_num_of_occupiers(facility_id):
    local_now = datetime.datetime.now(get_localzone())
    return (
        FacilityHistory.objects.filter(
            facility_id=facility_id, is_active=True, date_entered__lt=local_now
        )
        .filter(Q(date_left__isnull=True) | Q(date_left__gt=local_now))
        .count()
    )


class FacilityCompleteness(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if not FacilityUtils.has_rights(
            request.user.role,
            [
                "admin",
                "owner",
                "coordinator",
                "case_manager",
                "network_manager",
                "facility_manager",
            ],
        ):
            return Response("User has no permission", status=status.HTTP_403_FORBIDDEN)

        facility_id = kwargs.pop("pk", None)
        if facility_id is None:
            return Response(
                "We should pass a valid facility id", status=status.HTTP_404_NOT_FOUND
            )

        dict = {}
        dict["capacity"] = Facility.objects.get(pk=facility_id).capacity
        dict["occupants"] = get_num_of_occupiers(facility_id)

        return JsonResponse(dict)


class FacilityAddChild(APIView):
    permission_classes = (HasGeneralAdminPermissions, HasAddChildToFacilityPermissions)

    @staticmethod
    def get(request, *args, **kwargs):
        print("IUGUFUYF")
        facility_id = request.user.facility_id
        print(facility_id)
        if request.user.role == "admin":
            facility_id = request.query_params.get("facility_id", None)
        child_id = kwargs.pop("child_id", None)
        local_now = datetime.datetime.now(get_localzone())
        date_entered = request.query_params.get("date_entered", local_now)
        print("child_id")
        print(child_id)
        Facility.objects.add_child_to_facility(facility_id, child_id, date_entered)
        return Response(
            "Child: {} was added to facility: {}".format(child_id, facility_id),
            status=status.HTTP_200_OK,
        )


class FacilityRemoveChild(APIView):
    permission_classes = (
        HasGeneralAdminPermissions,
        HasRemoveChildToFacilityPermissions,
    )

    def post(self, request, *args, **kwargs):
        facility_id = request.user.facility_id
        if request.user.role == "admin":
            facility_id = request.query_params.get("facility_id", None)
        child_id = kwargs.pop("child_id", None)
        local_now = datetime.datetime.now(get_localzone())
        date_left = self.request.query_params.get("date_left", local_now)
        Facility.objects.remove_child_from_facility(facility_id, child_id, date_left)
        return Response(
            "The record of the child with id {} was updated".format(child_id),
            status=status.HTTP_200_OK,
        )


# Admin/Owner/Coordinator should be able to attach hosting facility manager to a facility
class FacilityAddManager(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        facility_id = kwargs.pop("pk", None)
        user_id = kwargs.pop("user_id", None)
        if facility_id is None:
            return Response(
                "We should pass a valid facility id", status=status.HTTP_404_NOT_FOUND
            )
        if user_id is None:
            return Response(
                "We should pass a valid user id", status=status.HTTP_404_NOT_FOUND
            )
        organization_id = Facility.objects.get(pk=facility_id).organization_id

        if not FacilityUtils.has_rights(
            request.user.role, ["admin", "owner", "coordinator"]
        ):
            return Response("User has no permission", status=status.HTTP_403_FORBIDDEN)

        if user_id is None or facility_id is None:
            return Response(
                "User and Facility parameters are required",
                status=status.HTTP_403_FORBIDDEN,
            )

        # 1.1 if its owner/coordinator, check if the organization he belongs is the same as the one to assign to
        # 1.2 check if the facility belongs to this organization
        if request.user.role in ["owner", "coordinator"]:
            if request.user.organization_id is None or str(
                request.user.organization_id
            ) != str(organization_id):
                return Response(
                    "User has no permission to this organization",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        # 1.3 if the facility does not belong to the organization or its inactive
        if not Facility.objects.filter(
            pk=facility_id, organization_id=organization_id, is_active=True
        ).exists():
            return Response(
                "This Facility does not belong to this organization or is not Active",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 2. check if user is HFM
        user = User.objects.get(pk=user_id)
        if user.role is not None and user.role != "facility_manager":
            return Response(
                "User role is not Hosting Facility Manager",
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. check if user is HFM and belongs to this organization
        if user.organization_id is None or str(user.organization_id) != str(
            organization_id
        ):
            return Response(
                "User belongs to a different organization",
                status=status.HTTP_403_FORBIDDEN,
            )

        # 4. check if HFM is already member of this facility
        if str(user.facility_id) == facility_id:
            return Response(
                "User id {} already belongs to the facility id {}".format(
                    user_id, facility_id
                ),
                status=status.HTTP_403_FORBIDDEN,
            )

        # 5. Assign
        user.facility_id = facility_id
        user.organization_id = organization_id
        user.save()

        return Response(
            "User: {} is assigned to facility: {}".format(user_id, facility_id),
            status=status.HTTP_200_OK,
        )


# Admin/Owner/Coordinator should be able to remove hosting facility manager to a facility
class FacilityRemoveManager(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        facility_id = kwargs.pop("pk", None)
        user_id = kwargs.pop("user_id", None)
        if facility_id is None:
            return Response(
                "We should pass a valid facility id", status=status.HTTP_404_NOT_FOUND
            )
        if user_id is None:
            return Response(
                "We should pass a valid user id", status=status.HTTP_404_NOT_FOUND
            )
        organization_id = Facility.objects.get(pk=facility_id).organization_id

        if not FacilityUtils.has_rights(
            request.user.role, ["admin", "owner", "coordinator"]
        ):
            return Response("User has no permission", status=status.HTTP_403_FORBIDDEN)

        if user_id is None or facility_id is None:
            return Response(
                "User and Facility parameters are required",
                status=status.HTTP_403_FORBIDDEN,
            )

        # 1.1 if its owner/coordinator, check if the organization he belongs is the same as the one to assign to
        # 1.2 check if the facility belongs to this organization
        if request.user.role in ["owner", "coordinator"]:
            if request.user.organization_id is None or str(
                request.user.organization_id
            ) != str(organization_id):
                return Response(
                    "User has no permission to this organization",
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        # 1.3 if the facility does not belong to the organization or its inactive
        if not Facility.objects.filter(
            pk=facility_id, organization_id=organization_id, is_active=True
        ).exists():
            return Response(
                "This Facility does not belong to this organization or is not Active",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 2. check if user is HFM
        user = User.objects.get(pk=user_id)
        if user.role is not None and user.role != "facility_manager":
            return Response(
                "User role is not Hosting Facility Manager",
                status=status.HTTP_403_FORBIDDEN,
            )

        # 3. check if user is HFM and belongs to this organization
        if user.organization_id is None or str(user.organization_id) != str(
            organization_id
        ):
            return Response(
                "User belongs to a different organization",
                status=status.HTTP_403_FORBIDDEN,
            )

        user.facility_id = None
        user.save()
        return Response(
            "User: {} is removed from facility: {}".format(user_id, facility_id),
            status=status.HTTP_200_OK,
        )
