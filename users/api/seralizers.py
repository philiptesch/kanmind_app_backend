from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Serializer for User profile information
class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)  # Read-only user ID
    fullname = serializers.SerializerMethodField()  # Computed full name of the user

    def get_fullname(self, obj):
        """
        Return the user's full name by combining first_name and last_name
        """
        return f"{obj.first_name} {obj.last_name}".strip()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']  # Fields returned in API


# Serializer for user information in comments
class UserCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()  # Display author full name

    def get_author(self, obj):
        """
        Return full name of the user who made the comment
        """
        return f"{obj.first_name} {obj.last_name}".strip()

    class Meta:
        model = User
        fields = ['author']  # Only include author field


# Serializer for user registration
class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)  # Password confirmation field
    fullname = serializers.CharField()  # Full name input field
    user_id = serializers.IntegerField(read_only=True)  # Read-only ID

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password', 'user_id']
        extra_kwargs = {'password': {'write_only': True}}  # Make password write-only

    def validate_email(self, value):
        """
        Validate that the email is unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate(self, data):
        """
        Ensure password and repeated_password match
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        """
        Create a new user with first_name and last_name extracted from fullname
        """
        fullname = validated_data.pop('fullname')
        name_parts = fullname.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create user instance
        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


# Serializer for custom login
class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Email field for login
    password = serializers.CharField(write_only=True)  # Password field

    def validate(self, data):
        """
        Validate login credentials and authenticate user
        """
        email = data.get('email')
        password = data.get('password')

        # Retrieve user by email
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Authenticate user using username (required by Django)
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        # Add authenticated user to validated data
        data['user'] = user
        return data
