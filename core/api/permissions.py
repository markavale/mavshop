from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

class AllowPost(BasePermission):
    permissions = ['GET', 'POST', ]
    def has_permission(self, request, view):
        return request.method in self.permissions