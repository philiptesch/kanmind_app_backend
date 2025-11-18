from .seralizers import BoardSerializer, BoardDetailSerializer, TaskSerializer, TaskAssignSerializer, TaskDetailSerializer, CommentSerializer,BoardDetailForPatchSerializer
from kanmind_board_app.models import Board, Task, Comment
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from .permisson import isMember, isAssigneeOrReviewer, isBoardOwnerorMember
from rest_framework.response import Response
from django.views.generic import ListView
from rest_framework import status
from django.shortcuts import get_object_or_404
class BoardsView(APIView):

    permission_classes =[IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(members=request.user) | Board.objects.filter(owner=request.user)
        serializer = BoardSerializer(boards, many=True)

        if not serializer.data:
            return Response({'message': 'Not authorized. The user must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)


            if not serializer.data:
                return Response({'message': 'Not authorized. The user must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class BoardDetailView(APIView):
    permission_classes =[isBoardOwnerorMember, IsAuthenticated]



    def get(self, request, pk):
          owner = Board.objects.filter(owner= request.user)
          members = Board.objects.filter(members= request.user)
          board = get_object_or_404(Board, pk=pk)
          if not owner and not members:
           return Response({'message': 'Not authorized. The user must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
          

          if request.user != board.owner and request.user not in board.members.all():
              return Response({'message': 'Forbidden. The user must either be a member of the board or the owner of the board.'}, status=status.HTTP_403_FORBIDDEN)

          if owner:
                serializer = BoardDetailSerializer(board)
                return Response(serializer.data, status=status.HTTP_200_OK)
          elif members:
                serializer = BoardDetailSerializer(board)
                return Response(serializer.data, status=status.HTTP_200_OK)
          

    def patch(self, request, pk):
          owner = Board.objects.filter(owner= request.user)
          members = Board.objects.filter(members= request.user)
          board = get_object_or_404(Board, pk=pk)
          if not owner and not members:
           return Response({'message': 'Not authorized. The user must be logged in'}, status=status.HTTP_401_UNAUTHORIZED)
          

          if request.user != board.owner and request.user not in board.members.all():
              return Response({'message': 'Forbidden. The user must either be a member of the board or the owner of the board.'}, status=status.HTTP_403_FORBIDDEN)
          

          serializer = BoardDetailForPatchSerializer(board, data=request.data, partial=True)


         # if board.owner.id not in request.data.get('members'):
           #     return Response({'message': 'The owner must be a member of the board.'}, status=400)

          if serializer.is_valid():
                serializer.save(owner_data=board.owner, members_data=board.members.all())
                return Response(serializer.data, status=200)

          return Response(serializer.errors, status=400)
    

    def delete(self, request, pk):
        board = get_object_or_404(Board, pk=pk)


        if not request.user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )


        if request.user != board.owner:
            return Response({'message': 'Forbidden. Only the owner can delete the board.'}, status=status.HTTP_403_FORBIDDEN)
        

        board.delete()
        return Response({'message': 'Board deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        email  = request.query_params.get('email') 

        if not email:
            return Response({'error': 'Email parameter is required.'}, status=400)
        
        if not user.is_authenticated:
            return Response({'error': 'Authentication required.'}, status=403)
        

        if user.email == email:
            return Response({
            'id': user.id,
            'fullname': user.get_full_name(),
            'email': email}, status=200)
        else:
            return Response({'error': 'Email does not match the authenticated user.'}, status=404)
        
 


        
class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated, isMember]

    def post(self, request, ):
        seralizer = TaskSerializer(data=request.data)

        board_id = request.data.get('board')
        

        if not request.user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )


        if not Board.objects.filter(id=board_id).exists():
            return Response({'message': 'Board id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in Board.objects.get(id=request.data.get('board')).members.all() and request.user != Board.objects.get(id=request.data.get('board')).owner:
            return Response({'message': 'Forbidden. The user must either be a member of the board or the owner of the board.'}, status=status.HTTP_403_FORBIDDEN)
        
        if seralizer.is_valid():

            task = seralizer.save(owner=request.user)
            return Response(seralizer.data, status=status.HTTP_201_CREATED)

        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskAssignView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isAssigneeOrReviewer]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskAssignSerializer(tasks,many=True)

        if not serializer.data: 
            return Response({'message': 'No tasks assigned to you.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data)        
    
class TaskReviewView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, isAssigneeOrReviewer]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskAssignSerializer(tasks,many=True)

        if not serializer.data: 
            return Response({'message': 'No tasks to review.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data)
    

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, isMember]

    def patch(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        board = task.board  

        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

        if request.user != board.owner and request.user not in board.members.all():
             return Response(
            {'detail': 'You are not allowed to modify this task.'},
            status=status.HTTP_403_FORBIDDEN
        )

        serializer = TaskDetailSerializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    
    def delete(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        board = task.board

        if not request.user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )
        
        if request.user != board.owner and request.user not in board.members.all():
            return Response(
            {'detail': 'You are not allowed to delete this task.'},
            status=status.HTTP_403_FORBIDDEN)

        task.delete()
        return Response(
        {'detail': 'The task was successfully deleted.'},
        status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    permission_classes = [IsAuthenticated, isMember]
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        board = task.board

        if not request.user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )
        
        if request.user != board.owner and request.user not in board.members.all():
            return Response(
            {'detail': 'You are not allowed to comment on this task.'},
            status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(author=request.user, task=task)
            response_serializer = CommentSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        task = get_object_or_404(Task, pk=pk)
        board = task.board

        if not user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )
        
        if request.user != board.owner and user not in board.members.all():
            return Response(
            {'detail': 'You are not allowed to comment on this task.'},
            status=status.HTTP_403_FORBIDDEN)
        comments = Comment.objects.filter(task=task)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated, isMember]

    def delete(self, request,task_id,  comment_id, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, pk=comment_id)
        commentOwner = comment.author

        if not request.user.is_authenticated:
            return Response(
            {'detail': 'Authentication credentials were not provided.'},
            status=status.HTTP_401_UNAUTHORIZED )
        
        if user != commentOwner:
            return Response(
            {'detail': 'You are not allowed to delete this comment.'},
            status=status.HTTP_403_FORBIDDEN)
        

        comment.delete()
        return Response(
        {'detail': 'The comment was successfully deleted.'},
        status=status.HTTP_204_NO_CONTENT)
    
