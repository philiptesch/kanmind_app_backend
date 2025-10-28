from django.urls import path, include
from .views import BoardsView

urlpatterns = [
 path('boards/',BoardsView.as_view(), name='boards-list-create')
]
