from .seralizers import BoardSerializer, BoardDetailSerializer
from kanmind_board_app.models import Board, Task, Comment
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny


class BoardsView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Board.objects.all()
    permission_classes =[AllowAny]
    serializer_class = BoardSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes =[AllowAny]
    serializer_class = BoardDetailSerializer



