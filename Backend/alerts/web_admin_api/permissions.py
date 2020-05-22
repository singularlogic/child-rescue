from django.shortcuts import get_object_or_404
from rest_framework import permissions

from alerts.models import Alert
from cases.models import Case


class HasAlertOrganizationAdminPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        """Works for every method."""
        organization = None
        if "pk" in view.kwargs:
            alert = get_object_or_404(Alert, id=view.kwargs["pk"])
            organization = alert.organization
        if "caseId" in request.query_params:
            case = get_object_or_404(Case, id=request.query_params["caseId"])
            organization = case.organization
        if "case" in request.data:
            case = get_object_or_404(Case, id=request.data["case"])
            organization = case.organization
        if organization is not None:
            if (
                request.user.organization_id is not None
                and request.user.organization_id != organization.id
            ):
                self.message = "User belong to different organization than the alert!"
                return False
            return True
        return request.user.organization_id is not None
