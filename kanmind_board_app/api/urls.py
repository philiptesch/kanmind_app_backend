from django.urls import path, include
from .views import BoardsView, BoardDetailView

urlpatterns = [
 path('boards/',BoardsView.as_view(), name='boards-list-create')
,path('boards/<int:pk>/',BoardDetailView.as_view(), name='board-detail')
 
]
