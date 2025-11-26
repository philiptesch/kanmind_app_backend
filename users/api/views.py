from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from users.api.seralizers import RegistrationSerializer, CustomLoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny


class RegisterrationView(generics.CreateAPIView):
    """
    View for registering new users.
    Accepts user data, validates it, and creates
    a new user upon success.
    Returns an auth token and user info afterwards.
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        POST a new user with token-key, fullname, id and email-adress
        """
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
    """
    View for authenticating users via email and password.
    Uses CustomAuthTokenSerializer to validate credentials.
    On successful login, returns an auth token along with
    user information (full name, email, user ID and token-key).
    """
    serializer_class = CustomLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        POST to login a existing user 
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            fullname = f"{user.first_name} {user.last_name}".strip()
            return Response({
            "message": "Login successful",
            "fullname": fullname,
            "email": user.email,
            "token": token.key,
            "user_id": user.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)