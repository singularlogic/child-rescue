from django.shortcuts import get_object_or_404
from rest_framework import permissions
from cases.models import Case, Child


class HasOrganizationPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if "pk" in view.kwargs:
            case = get_object_or_404(Case, id=view.kwargs["pk"])
            if (
                request.user.organization_id is not None
                and request.user.organization_id != case.organization_id
            ):
                self.message = "User does not belong to case organisation!"
                return False
        return True


class HasCloseCasePermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        case = get_object_or_404(Case, pk=view.kwargs["pk"])
        if case.status != "active":
            self.message = "Selected case is not active, so it cannot be closed!"
            return False
        return True


class HasArchiveCasePermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        case = get_object_or_404(Case, pk=view.kwargs["pk"])
        if (
            case.status != "closed"
        ):  # check dis type, is_refugee and facts (valid/invalid)
            self.message = "Selected case is not closed, so it cannot be archived!"
            return False
        return True


class HasFacilityCasePermissionObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.status != "inactive"
            or obj.facility.first().id == request.user.facility.id
        )


class FacilityCaseStatePermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        case = Case.objects.get(pk=view.kwargs["pk"])
        presence_status = request.query_params.get("presence_status", None)
        if request.user.organization_id != case.organization_id:
            self.message = "User does not belong to case organisation!"
            return False
        if case.status == "active":
            self.message = "Case is active and cannot change present state!"
            return False
        if str(case.presence_status) == str(presence_status):
            self.message = "Case is already {}!".format(presence_status)
            return False
        return True
