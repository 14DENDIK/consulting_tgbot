from rest_framework import permissions

class IsStaffOrPostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return not request.user.is_anonymous
        return True
