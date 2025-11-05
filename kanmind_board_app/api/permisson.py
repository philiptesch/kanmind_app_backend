from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView



class isMember(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user)


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user in obj.members.all()
    

class isBoardOwnerorMember(BasePermission):

        def has_object_permission(self, request, view, obj):
            if request.method in SAFE_METHODS:
                return True
            return request.user == obj.owner or request.user in obj.members.all()
        
        
    
class isAssigneeOrReviewer(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.assignee or request.user == obj.reviewer