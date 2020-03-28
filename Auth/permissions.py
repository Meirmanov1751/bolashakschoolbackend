from rest_framework import permissions


class CreateAndIsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if (view.action == 'create'):
            return True
        return super(CreateAndIsAuthenticated, self).has_permission(request, view)
