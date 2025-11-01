from django.urls import path, include
from django.urls import path
from .views import RegisterrationView

urlpatterns = [
    path('registration/', RegisterrationView.as_view(), name='registration'),
 
]