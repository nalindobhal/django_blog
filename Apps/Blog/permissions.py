from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    message = 'You are not authorized'

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.published_by == request.user
