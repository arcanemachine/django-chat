from rest_framework import permissions

from chat.models import Message


class HasMessagePermissionsOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        message = obj
        if type(obj) != Message:
            raise TypeError(
                "This permission can only be used with a Message object")
        if not request.user.is_authenticated:
            return False
        elif request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        elif message.sender == request.user:
            return True
        else:
            return False


class HasMessagePermissionsOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        message = obj
        if type(obj) != Message:
            raise TypeError(
                "This permission can only be used with a Message object")
        if not request.user.is_authenticated:
            return False
        elif request.user.is_staff:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        elif message.sender == request.user:
            return True
        else:
            return False
