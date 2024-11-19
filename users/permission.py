from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStudent(BasePermission):
    """Allows access only to students for their own records."""

    def has_object_permission(self, request, view, obj):
        # Students can view/update their own records
        return request.user.role == 'Student' and obj.user == request.user


class IsTeacher(BasePermission):
    """Allows access to teachers for specific actions."""

    def has_permission(self, request, view):
        # Teachers can perform any non-destructive actions (e.g., POST, PUT)
        return request.user.role == 'Teacher'

    def has_object_permission(self, request, view, obj):
        # Teachers can access any related objects they manage
        return request.user.role == 'Teacher'


class IsAdmin(BasePermission):
    """Allows access to admins for all actions."""

    def has_permission(self, request, view):
        return request.user.role == 'Admin'
