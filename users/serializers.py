from rest_framework import serializers
from .models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'role'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'bio',
            'image'
            ]
        read_only_fields = ['id', 'user']

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
