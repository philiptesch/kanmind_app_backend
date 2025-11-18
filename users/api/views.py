from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import UserProfile
from rest_framework import generics, status
from users.api.seralizers import RegistrationSerializer, CustomLoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User



class RegisterrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        saved_account = serializer.save()
        fullname = f"{saved_account.first_name} {saved_account.last_name}".strip()
        token, created = Token.objects.get_or_create(user=saved_account)
        
        return Response({
            "message": "User registered successfully",
            'fullname': fullname,
            'email': saved_account.email,
            'token': token.key,
            'user_id': saved_account.id
        })
    


class CustomLogin(ObtainAuthToken):
    serializer_class = CustomLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            profile, _ = UserProfile.objects.get_or_create(user=user)
            fullname = f"{user.first_name} {user.last_name}".strip()
            return Response({
            "message": "Login successful",
            "fullname": fullname,
            "email": user.email,
            "token": token.key,
            "user_id": user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)