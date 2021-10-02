"""Permissions"""
from rest_framework import permissions
from .models import Employee


class IsAuthenticatedAndAdminUser(permissions.BasePermission):

      def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.employee.role == "A"
      return False

class IsAuthenticatedAndGestorUser(permissions.BasePermission):

      def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.employee.role == "G"
      return False
