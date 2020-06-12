from rest_framework import status, permissions
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class IsOwnerOrReadOnly(BasePermission):
    message = Response(status=status.HTTP_403_FORBIDDEN)
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.author == request.user
        else:
            return True