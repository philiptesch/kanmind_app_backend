from .seralizers import (
    BoardSerializer, BoardDetailSerializer, TaskSerializer, TaskAssignOrReviewerSerializer,
    TaskDetailSerializer, CommentSerializer, BoardDetailForPatchSerializer,
    CommentResponseSerializer
)
from kanmind_board_app.models import Board, Task, Comment
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permisson import isMember, isAssigneeOrReviewer, isBoardOwnerorMember
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q



class BoardsView(APIView):
    """
    API view for listing and creating boards.
    GET: Returns all boards where the user is a member or owner.
    POST: Creates a new board with the logged-in user as the owner.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET:
        - Returns boards where the user is owner or member.
        - Includes counts: members, tasks, tasks to do, high-priority tasks.
        """
        boards = Board.objects.filter(Q(members=request.user) | Q(owner=request.user)).distinct()
        serializer = BoardSerializer(boards, many=True)

        if not serializer.data:
            return Response({'message': 'No boards found or not authorized.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data)

    def post(self, request):
        """
        POST:
         - Serializer: BoardSerializer (overview)
        - Creates a new board with the authenticated user as owner.
        - Expects 'title' and optionally 'members' as IDs.
        """
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    """
    API view for retrieving details, updating (PATCH), and deleting a board.
    Access rights: Only board owners or members.
    """
    permission_classes = [isBoardOwnerorMember, IsAuthenticated]

    def get(self, request, pk):
        """
         GET:
        - (includes full tasks list)
        - Returns board details with members and tasks.
        """
        board = get_object_or_404(Board, pk=pk)

        if request.user != board.owner and request.user not in board.members.all():
            return Response({'message': 'Forbidden. Only owner or members can access this board.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BoardDetailSerializer(board)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """
        PATCH:
        - Update optional fields: `title`, `members` (IDs)
        - Response includes read-only: `owner_data`, `members_data`
        """
        board = get_object_or_404(Board, pk=pk)

        if request.user != board.owner and request.user not in board.members.all():
            return Response({'message': 'Forbidden. Only owner or members can update this board.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BoardDetailForPatchSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner_data=board.owner, members_data=board.members.all())
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """"
        DELETE:
        - No serializer needed.
        - Deletes the board if user is owner
        """ 
        board = get_object_or_404(Board, pk=pk)

        if request.user != board.owner:
            return Response({'message': 'Forbidden. Only owner can delete this board.'}, status=status.HTTP_403_FORBIDDEN)

        board.delete()
        return Response({'message': 'Board deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



class EmailCheckView(APIView):
    """
    Check if provided email matches the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET:
        - Query param: 'email'
        - Returns user ID, full name, and email if matches
        """
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email parameter is required.'}, status=400)

        user = request.user
        if user.email == email:
            return Response({
                'id': user.id,
                'fullname': user.get_full_name(),
                'email': email
            }, status=200)
        else:
            return Response({'error': 'Email does not match authenticated user.'}, status=404)


class TaskCreateView(APIView):
    """
    Create a task in a board.
    - Only board members or owner can create tasks.
    """
    permission_classes = [IsAuthenticated, isMember]

    def post(self, request):
        """  
        POST:
        - Required: board ID, assignee_id, reviewer_id, title, due_date
        - Automatically sets authenticated user as task owner
        - assignee_id and reviewer_id must be existing user
        """
        serializer = TaskSerializer(data=request.data)
        board_id = request.data.get('board')
        assignee_id = request.data.get('assignee_id')
        reviewer_id = request.data.get('reviewer_id')

        if not isinstance(assignee_id, int) or not isinstance(reviewer_id, int):
            return Response({'detail': 'assignee_id and reviewer_id must be integers.'}, status=400)
        if not (User.objects.filter(id=assignee_id).exists() and User.objects.filter(id=reviewer_id).exists()):
            return Response({'detail': 'Assignee or reviewer does not exist.'}, status=400)
        if not Board.objects.filter(id=board_id).exists():
            return Response({'message': 'Board id does not exist'}, status=404)

        board = Board.objects.get(id=board_id)
        if request.user not in board.members.all() and request.user != board.owner:
            return Response({'message': 'Forbidden. Must be a member or owner of board.'}, status=403)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TaskAssignView(generics.ListCreateAPIView):
    """
    List all tasks assigned to the authenticated user.
    """
    permission_classes = [IsAuthenticated, isAssigneeOrReviewer]

    def get(self, request):
        """
        GET:
        - Returns tasks where user is assignee
        """
        user = request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskAssignOrReviewerSerializer(tasks, many=True)
        if not serializer.data:
            return Response({'message': 'No tasks assigned.'}, status=401)
        return Response(serializer.data)


class TaskReviewView(generics.ListCreateAPIView):
    """
    List all tasks the authenticated user is assigned to review.

    """
    permission_classes = [IsAuthenticated, isAssigneeOrReviewer]

    def get(self, request):
        """
        GET:
        - Returns tasks where user is reviewer
        """
        user = request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskAssignOrReviewerSerializer(tasks, many=True)
        if not serializer.data:
            return Response({'message': 'No tasks to review.'}, status=401)
        return Response(serializer.data)


class TaskDetailView(APIView):
    """
    Retrieve, update, or delete a specific task.
    - Only task creators or board owners can make changes
    """
    permission_classes = [IsAuthenticated, isMember]

    def patch(self, request, pk, *args, **kwargs):
        """ 
        PATCH:
        - Updates task fields 
        - Only task creators or board owners can update a task
        """
        task = get_object_or_404(Task, pk=pk)
        board = task.board
        if request.user != board.owner and request.user not in board.members.all():
            return Response({'detail': 'Cannot modify task.'}, status=403)

        serializer = TaskDetailSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        """ 
        DELETE:
        - deletes task
        - Only task creators or board owners can delete a task
        """
        task = get_object_or_404(Task, pk=pk)
        board = task.board
        if request.user != board.owner and request.user not in board.members.all():
            return Response({'detail': 'Cannot delete task.'}, status=403)
        task.delete()
        return Response({'detail': 'Task deleted successfully.'}, status=204)


class CommentView(APIView):
    """
    Create or list comments for a task.
    - Only board members or owner can comment or view comments
    """
    permission_classes = [IsAuthenticated, isMember]

    def post(self, request, pk, *args, **kwargs):
        """
        POST:
        - Serializer: CommentSerializer (input)
        - Serializer: CommentResponseSerializer (output)
        - Field allowed: 'content' only
        """
        task = get_object_or_404(Task, pk=pk)
        board = task.board

        extra_fields = set(request.data.keys()) - {'content'}
        if extra_fields:
            return Response({'detail': f'Extra fields not allowed: {extra_fields}'}, status=400)

        content = request.data.get('content', '').strip()
        if not content:
            return Response({'detail': 'Content is empty.'}, status=400)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, task=task)
            response_serializer = CommentResponseSerializer(comment)
            return Response(response_serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, pk, *args, **kwargs):
        """
        GET:
        - Lists all comments for a task
        - Only board `owner` or `members` can view
    
        """
        task = get_object_or_404(Task, pk=pk)
        board = task.board

        comments = Comment.objects.filter(task=task)
        serializer = CommentResponseSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class CommentDeleteView(APIView):
    """
    Delete a comment.
    - Only comment author can delete.
    """
    permission_classes = [IsAuthenticated, isMember]

    def delete(self, request, task_id, comment_id, *args, **kwargs):
        """ 
        DELETE:
        - deletes comments
        """
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)
        if request.user != comment.author:
            return Response({'detail': 'Cannot delete comment.'}, status=403)
        comment.delete()
        return Response({'detail': 'Comment deleted successfully.'}, status=204)
