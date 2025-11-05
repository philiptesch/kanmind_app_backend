from django.urls import path, include
from .views import BoardsView, BoardDetailView, EmailCheckView, TaskCreateView, TaskAssignView, TaskReviewView

urlpatterns = [
 path('boards/',BoardsView.as_view(), name='boards-list-create'),
 path('boards/<int:pk>/',BoardDetailView.as_view(), name='board-detail'),
 path('email-check/', EmailCheckView.as_view(), name='email-check'),
 path('tasks/', TaskCreateView.as_view(), name='task-create'),
 path('tasks/assigned-to-me/', TaskAssignView.as_view() , name='tasks-assigned-to-me'),
 path('tasks/reviewing/', TaskReviewView.as_view() , name='tasks-reviewing'),
 
]
