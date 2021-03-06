from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        """Validation for User."""

        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters.')
        
        return attrs

    def create(self, validated_data):
        """Create user with validated data."""
        return User.objects.create_user(**validated_data)

        return super().validate(attrs)
        

class EmailVerifaicationSerializer(serializers.ModelSerializer):
    """Serializer for email verification with token."""
    token = serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token']


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=555, read_only= True)



    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, Try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')
        

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }