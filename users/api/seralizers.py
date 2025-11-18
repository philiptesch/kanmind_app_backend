from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):   
    id = serializers.IntegerField(read_only=True)
    fullname = serializers.SerializerMethodField()
    
    def get_fullname(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email']

class UserCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    

    class Meta:
        model = User
        fields = ['author']

        


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField()
    user_id = serializers.IntegerField(read_only=True,)
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password', 'user_id']
        extra_kwargs = {'password': {'write_only': True}}



    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value


    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data


    def create(self, validated_data):
        fullname = validated_data.pop('fullname')
        name_parts = fullname.strip().split(" ", 1)
        first_name = name_parts[0]

        last_name = name_parts[1] if len(name_parts) > 1 else ""
        user = User(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        data['user'] = user
        return data