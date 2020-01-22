from rest_framework import permissions

from cases.models import CaseVolunteer


class HasVolunteerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # CaseVolunteer.objects.filter(user=request.user, case=1, has_accept_invitation=True)
        return request.user.role == "volunteer"
