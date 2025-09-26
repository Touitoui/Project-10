from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Contributor

 
class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        ''' Check if the user is authenticated and is an admin (superuser) '''
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        ''' Check if the user is the author of the object '''
        print(f"Checking author permission for user {request.user} on object {obj}")
        print(f"Object author: {obj.author}, Request user: {request.user}")

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `author`.
        return obj.author == request.user


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        ''' Check if the user is a contributor to the project specified in the request data, ignore if no project specified '''

        if request.method in SAFE_METHODS:
            return True
        
        if not request.data.get('project'):
            return True
        return Contributor.objects.filter(user=request.user, project=request.data.get('project')).exists()
        
    def has_object_permission(self, request, view, obj):
        ''' Check if the user is a contributor to the project of the object '''

        project = None
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project

        if request.method in SAFE_METHODS:
            return True

        return Contributor.objects.filter(user=request.user, project=project).exists() and obj.author == request.user
