import datetime

from django.shortcuts import get_object_or_404
from tzlocal import get_localzone
from django.db.models import Q
from rest_framework import permissions

from cases.models import FacilityHistory, Case
from facilities.models import Facility


class HasFacilityPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get("pk", None)
        is_admin = request.user.role == "admin"
        is_organization_manager = request.user.role == "organization_manager"

        if request.method == "GET" and pk is None:
            return is_admin or is_organization_manager
        else:
            belongs_to_organization_post = request.data.get("organization", None) == request.user.organization_id
            if pk is not None:
                belongs_to_organization_get = (
                    get_object_or_404(Facility, id=pk).organization == request.user.organization
                )
                belongs_to_organization = belongs_to_organization_get or belongs_to_organization_post
            else:
                belongs_to_organization = belongs_to_organization_post
            return is_admin or (is_organization_manager and belongs_to_organization)


class BaseChildFacilityPermissions(permissions.BasePermission):
    message = "Permission denied!"

    def common(self, request, facility_id):
        organization_id = Facility.objects.get(pk=facility_id).organization_id
        if request.user.role is not None and request.user.role != "admin":
            if request.user.organization_id is None or request.user.organization_id != organization_id:
                self.message = "User has no permission to this organization!"
                return False

        if request.user.role in ["facility_manager"]:
            if request.user.facility_id is None or request.user.facility_id != facility_id:
                self.message = "User has no permission to this facility!"
                return False

        if not Facility.objects.filter(
            pk=facility_id, organization_id=organization_id, supports_hosting=True, is_active=True,
        ).exists():
            self.message = "Facility does not exist | not part of the organization | not active | not support hosting!"
            return False
        return True


class HasRemoveChildToFacilityPermissions(BaseChildFacilityPermissions):
    def has_permission(self, request, view):
        facility_id = request.user.facility_id
        if request.user.role == "admin":
            facility_id = request.query_params.get("facility_id", None)
        child_id = view.kwargs["child_id"]
        if facility_id is None or child_id is None:
            self.message = "facility_id or child_id is null"
            return False
        cases_objects = FacilityHistory.objects.filter(case_id=child_id, facility_id=facility_id, is_active=True)
        if not cases_objects.exists():
            self.message = "Child was never accommodated in this facility"
            return False
        return self.common(request, facility_id)


class HasAddChildToFacilityPermissions(BaseChildFacilityPermissions):
    @staticmethod
    def get_num_of_occupiers(facility_id):
        local_now = datetime.datetime.now(get_localzone())
        return (
            FacilityHistory.objects.filter(facility_id=facility_id, is_active=True, date_entered__lt=local_now)
            .filter(Q(date_left__isnull=True) | Q(date_left__gt=local_now))
            .count()
        )

    def has_permission(self, request, view):
        facility_id = request.user.facility_id
        if request.user.role == "admin":
            facility_id = request.query_params.get("facility_id", None)
        child_id = view.kwargs["child_id"]
        num_of_occupiers = self.get_num_of_occupiers(facility_id)

        if facility_id is None or child_id is None:
            self.message = "facility_id or child_id is null"
            return False

        capacity = Facility.objects.get(pk=facility_id).capacity
        # case = get_object_or_404(Case, child=child_id)
        case = Case.objects.filter(child=child_id).last()
        if FacilityHistory.objects.filter(facility__id=facility_id, case__id=case.id, date_left__isnull=True).exists():
            self.message = "This child is already registered in this facility!"
            return False

        if num_of_occupiers >= capacity:
            self.message = "Facility cannot accommodate any more children!"
            return False

        return self.common(request, facility_id)
