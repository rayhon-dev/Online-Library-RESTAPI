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
        password = attrs.get('password')
        password2 = self.initial_data.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return CustomUser.objects.create_user(**validated_data)

