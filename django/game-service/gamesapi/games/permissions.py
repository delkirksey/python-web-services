from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Grants read-only access to non-owner users. Grants
    full permissions to owners of an object
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user
