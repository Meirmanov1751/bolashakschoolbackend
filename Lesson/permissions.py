from rest_framework import permissions


class IsActiveAndIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return(
            request.user.is_active and
            super(IsActiveAndIsAuthenticated, self).has_permission(request, view)
        )
