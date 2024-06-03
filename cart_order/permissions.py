from rest_framework import permissions

class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if hasattr(user, 'charity') and user.charity == obj.charity:
            return True
        
        return False

class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if hasattr(request.user, 'charity') and request.user.charity == obj.charity:
            return True
        
        return False
