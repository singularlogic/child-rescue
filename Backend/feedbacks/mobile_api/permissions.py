from rest_framework import permissions


class HasMobileFeedbackPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        elif request.method == "GET":
            if request.user.is_authenticated:
                return True
            else:
                return False
        else:
            return False
