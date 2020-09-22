from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

class AllowPost(BasePermission):
    permissions = ['GET', 'POST', ]
    def has_permission(self, request, view):
        return request.method in self.permissions

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsMemberOrIpAddressOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    methods = ['GET', 'POST', 'DELETE']
    
    def has_object_permission(self, request, view, obj):
        ip_addr = request.META['REMOTE_ADDR']
        if request.method in self.methods:
            return True
        return obj.ip_address == ip_addr