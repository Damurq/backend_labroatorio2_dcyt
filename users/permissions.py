"""Permissions"""
from rest_framework import permissions
from django.contrib.auth.models import User

class IsUserActivate(permissions.BasePermission):
      def has_permission(self, request, view):
            try:
                  status = User.objects.get(username=request.data["username"]).status
                  if status:
                        return True
            except Exception:
                  return False
            return False

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
