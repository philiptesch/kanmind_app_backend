from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from users.models import UserProfile
from rest_framework import generics, status
from users.api.seralizer import RegistrationSerializer



class RegisterrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        saved_account = serializer.save()
        token, created = Token.objects.get_or_create(user=saved_account)
        profile = UserProfile.objects.get(user=saved_account)
        return Response({
            "message": "User registered successfully",
            'fullname': profile.fullname,
            'email': saved_account.email,
            'password': saved_account.password,
            'token': token.key,
        })
