from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from rest_framework import serializers
from .models import User
import re

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if username:
            name_data = username
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:1234567890]')
            if not regex.search(name_data) == None:
                raise serializers.ValidationError({'error':'name cannot be numeric'})
        
        return data
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=100, write_only=True)
    username = serializers.CharField(max_length=100, read_only=True)
    tokens = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, data):
        email = data.get('email').lower()
        password = data.get('password')

        print(f'{email} and {password}')
        user = User.objects.get(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact to admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username' : user.username,
            'tokens' : user.token
        }
    
        