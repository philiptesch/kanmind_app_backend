from rest_framework.permissions import BasePermission, SAFE_METHODS

# Permission to check if the user is a member of an object (e.g., Board)
class isMember(BasePermission):

    def has_permission(self, request, view):
        """
        Check general permission:
        - Allow all safe methods (GET, HEAD, OPTIONS)
        - Require authenticated user for other methods
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission:
        - Allow all safe methods
        - For other methods, the user must be in the object's members
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.members.all()
    

# Permission to check if the user is the owner or a member of a board
class isBoardOwnerorMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Allow safe methods
        - Otherwise, user must be the owner or a member
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner or request.user in obj.members.all()
        

# Permission to check if the user is either the assignee or reviewer of a task
class isAssigneeOrReviewer(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Allow safe methods
        - Otherwise, user must be the assignee or the reviewer
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.assignee or request.user == obj.reviewer
