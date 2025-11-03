from django.urls import path, include
from .views import BoardsView, BoardDetailView, EmailCheckView

urlpatterns = [
 path('boards/',BoardsView.as_view(), name='boards-list-create'),
 path('boards/<int:pk>/',BoardDetailView.as_view(), name='board-detail'),
 path('email-check/', EmailCheckView.as_view(), name='email-check')
 
]
