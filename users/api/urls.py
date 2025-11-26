from django.urls import path
from django.urls import path
from .views import RegisterrationView, CustomLogin

urlpatterns = [
    path('registration/', RegisterrationView.as_view(), name='registration'),
    path('login/', CustomLogin.as_view(), name='login'),
 
]