from rest_framework import permissions


class OrganizationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class CreateUserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = request.user.role == "admin"
        is_organization_manager = request.user.role == "organization_manager"
        belongs_to_organization = request.user.organization.id == obj if not is_admin else False
        return is_admin or (is_organization_manager and belongs_to_organization)


class OrganizationObjectPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = request.user.role == "admin"
        is_organization_manager = request.user.role == "organization_manager"

        belongs_to_organization = request.user.organization.id == obj.id if not is_admin else False
        if request.method == "GET":
            return belongs_to_organization
        elif request.method == "DELETE":
            return is_admin
        else:
            return is_admin or (is_organization_manager and belongs_to_organization)
