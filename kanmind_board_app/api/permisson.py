from rest_framework.permissions import BasePermission, SAFE_METHODS

class isMember(BasePermission):

    def has_permission(self, request, view):
        """
        Check general permission:
        - Require authenticated user for other methods
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission:
        - For other methods, the user must be in the object's members
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.members.all()
    


class isBoardOwnerorMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Otherwise, user must be the owner or a member
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner or request.user in obj.members.all()
        

class isAssigneeOrReviewer(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Otherwise, user must be the assignee or the reviewer
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.assignee or request.user == obj.reviewer
