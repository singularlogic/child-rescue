from django.shortcuts import get_object_or_404
from rest_framework import permissions

from alerts.models import Alert
from cases.models import Case, SharedCase


class HasAlertOrganizationAdminPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):
        """Works for every method."""
        organization = None
        case = None
        if "pk" in view.kwargs:
            alert = get_object_or_404(Alert, id=view.kwargs["pk"])
            case = alert.case
            organization = alert.organization
        if "caseId" in request.query_params:
            case = get_object_or_404(Case, id=request.query_params["caseId"])
            organization = case.organization
        if "case" in request.data:
            case = get_object_or_404(Case, id=request.data["case"])
            organization = case.organization
        if organization is not None:
            shared_case = SharedCase.objects.filter(case=case).first()
            is_shared_case = False
            if shared_case is not None and request.user.organization_id is not None:
                is_shared_case = request.user.organization_id == shared_case.organization.id
            if (
                request.user.organization_id is not None
                and (request.user.organization_id != organization.id and not is_shared_case)
            ):
                self.message = "User belong to different organization than the alert!"
                return False
            return True
        return request.user.organization_id is not None
