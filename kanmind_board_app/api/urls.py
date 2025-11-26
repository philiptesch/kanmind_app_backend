from django.urls import path
from .views import BoardsView, BoardDetailView, EmailCheckView, TaskCreateView, TaskAssignView, TaskReviewView,TaskDetailView, CommentView, CommentDeleteView

urlpatterns = [
 path('boards/',BoardsView.as_view(), name='boards-list-create'),
 path('boards/<int:pk>/',BoardDetailView.as_view(), name='board-detail'),
 path('email-check/', EmailCheckView.as_view(), name='email-check'),
 path('tasks/', TaskCreateView.as_view(), name='task-create'),
 path('tasks/assigned-to-me/', TaskAssignView.as_view() , name='tasks-assigned-to-me'),
 path('tasks/reviewing/', TaskReviewView.as_view() , name='tasks-reviewing'),
 path('tasks/<int:pk>/', TaskDetailView.as_view() , name='task-detail'),
 path('tasks/<int:pk>/comments/', CommentView.as_view() , name='comments'),
 path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view() , name='comment-delete'),
]
