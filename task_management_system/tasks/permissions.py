from rest_framework.permissions import BasePermission


# created custom permissions to check is admin or not.
class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"
