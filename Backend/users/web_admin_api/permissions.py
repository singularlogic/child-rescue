from django.shortcuts import get_object_or_404
from rest_framework import permissions

from facilities.models import Facility


class UserPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        is_admin = request.user.role == "admin"
        is_organization_manager = request.user.role == "organization_manager"
        belongs_to_organization = request.user.organization is not None
        if request.method == "POST":
            role = request.data.get("role", None)
            organization = request.data.get("organization", None)
            facility = request.data.get("facility", None)
            if is_organization_manager:
                organization = request.user.organization
            if role is not None and role != "simple_user":
                if organization is None:
                    self.message = "Admin type users must have organization!"
                    return False
            if role != "volunteer":
                if facility is None:
                    self.message = "Admin type users must have facility!"
                    return False
                if not isinstance(organization, int):
                    organization = organization.id
                if (
                    get_object_or_404(Facility, id=facility).organization.id
                    != organization
                ):
                    self.message = "Facility must belong to user organization"
                    return False
            return is_admin or (is_organization_manager and belongs_to_organization)
        else:
            return is_admin or belongs_to_organization


class UserObjectPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = request.user.role == "admin"
        is_organization_manager = request.user.role == "organization_manager"
        belongs_to_organization = (
            request.user.organization == obj.organization if not is_admin else True
        )
        if request.method == "GET":
            return belongs_to_organization
        elif request.method == "DELETE":
            return is_admin
        else:
            return is_admin or (is_organization_manager and belongs_to_organization)


class HasGeneralAdminPermissions(permissions.BasePermission):
    """
    User must be authenticated and has an admin role!
    """

    message = "Permission denied!"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            self.message = "User is not authenticated!"
            return False
        if request.user.role is None and request.user.role not in [
            "admin",
            "organization_manager",
            "coordinator",
            "case_manager",
            "network_manager",
            "facility_manager",
        ]:
            self.message = "User has not proper admin rights!"
            return False
        return True


class HasCaseManagerPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if request.user.role is None:
            return False
        is_manager = request.user.role in [
            "organization_manager",
            "coordinator",
            "network_manager",
            "case_manager",
            "facility_manager",
        ]
        is_case_manager = request.user.role in [
            "organization_manager",
            "coordinator",
            "case_manager",
            "facility_manager",
        ]

        if request.method == "GET":
            return is_manager
        else:
            return is_case_manager


class HasNetworkManagerPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if request.user.role is None:
            return False
        is_manager = request.user.role in [
            "organization_manager",
            "coordinator",
            "network_manager",
            "case_manager",
            "facility_manager",
        ]
        is_network_manager = request.user.role in [
            "organization_manager",
            "coordinator",
            "network_manager",
        ]

        if request.method == "GET":
            return is_manager
        else:
            return is_network_manager
