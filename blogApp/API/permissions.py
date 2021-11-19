from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        methods = ['PUT','PATCH']
        if request.method in methods : 
            return obj.author == request.user
        
        return True