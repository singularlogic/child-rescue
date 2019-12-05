from django.shortcuts import get_object_or_404
from rest_framework import permissions

from cases.models import Case
from places.models import Place


class HasPlacePermissions(permissions.BasePermission):
    message = "Permission denied!"

    def has_permission(self, request, view):

        def _check_permissions(_user, _case):
            _has_proper_role = _user.role in ["organization_manager", "coordinator", "case_manager", "network_manager"]
            _belongs_to_organization = _case.organization == _user.organization
            if _has_proper_role and _belongs_to_organization:
                return True
            return False

        if request.method in ["POST"]:
            case_id = request.data.get('case', None)
            case = get_object_or_404(Case, id=case_id)
            return _check_permissions(request.user, case)
        elif request.method in ["DELETE", "PATCH", "PUT"]:
            place = get_object_or_404(Place, id=view.kwargs["pk"])
            return _check_permissions(request.user, place.case)
        else:
            if not request.user.is_authenticated:
                return False
            case_id = request.query_params.get('caseId', None) or view.kwargs["pk"]
            case = get_object_or_404(Case, id=case_id)
            return case.organization == request.user.organization
