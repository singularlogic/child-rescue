from django.shortcuts import get_object_or_404
from rest_framework import permissions

from alerts.models import Alert
from cases.models import Case


class HasAlertOrganizationAdminPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if request.user.role != "admin":
            alert = Alert.objects.get(pk=view.kwargs["pk"])
            if request.user.organization_id is None or str(
                request.user.organization_id
            ) != str(alert.organization.id):
                self.message = "User belong to different organization than the fact!"
                return False
        return True


class HasGetAlertPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        is_super_admin = request.user.organization_id is None
        if request.method == "GET":
            if not is_super_admin:
                case_id = request.query_params.get("caseId", None)
                if case_id is not None:
                    is_case_in_same_organization = (
                        get_object_or_404(Case, pk=case_id).organization.id
                        == request.user.organization_id
                    )
                    if not is_case_in_same_organization:
                        self.message = (
                            "Case belong to different organization than the user!"
                        )
                        return False
        return True


class HasCreateAlertPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if request.method == "POST":
            case_id = request.data["case"] if "case" in request.data else None
            if case_id is None:
                self.message = "You must provide a case id!"
                return False
            if (
                Case.objects.get(id=case_id).organization.id
                != request.user.organization_id
            ):
                self.message = "Case belong to different organization than the user!"
                return False
        return True


class HasDeleteAlertPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        if request.method == "DELETE":
            if request.user.role != "admin":
                self.message = "Only admin can delete alerts!"
                return False
        return True
