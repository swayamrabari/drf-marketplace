from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to edit objects,
    while allowing read-only access for other users.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow only the owner of an object or admin users to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if obj.user != request.user:
            return False

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if view.action == 'cancel':
            return True

        return False
