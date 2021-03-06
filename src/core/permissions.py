from rest_framework import permissions

class IsDomainAdminOrStaff(permissions.BasePermission):
    """
    Global permission to make sure that the user requesting a given action is actually a domain administrator or a staff member
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_domain_admin or request.user.is_staff)

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin