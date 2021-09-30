"""Permissions"""
from rest_framework import permissions
from .models import Employee


class IsAuthenticatedAndAdminUser(permissions.BasePermission):

      def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            emp=Employee.objects.get(user=user.id)
            return emp.role=="A"
        return False

class IsAuthenticatedAndNotAdminUser(permissions.BasePermission):

      def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            emp=Employee.objects.get(user=user.id)
            return emp.role=="G"
        return False

class AllowAnyUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return permissions.AllowAny
