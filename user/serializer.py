from datetime import datetime

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    birthday = serializers.DateField(input_formats=['%d-%m-%Y', '%d.%m.%Y'])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birthday', 'profile_image', 'password', 'confirm_password', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('birthday'):
            birthday = datetime.strptime(representation['birthday'], '%Y-%m-%d')
            representation['birthday'] = birthday.strftime('%d.%m.%Y')
        return representation


class UserProfileSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(input_formats=['%d-%m-%Y', '%d.%m.%Y'])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'birthday', 'profile_image', 'date_joined']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'profile_image': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('birthday'):
            birthday = datetime.strptime(representation['birthday'], '%Y-%m-%d')
            representation['birthday'] = birthday.strftime('%d.%m.%Y')
        return representation


class UserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect password"})

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": "Passwords do not match"})

        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class LoginProfileSerializer(UserSerializer):

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        user.last_login = now()
        user.save(update_fields=['last_login'])
        data['user'] = LoginProfileSerializer(self.user, context={'request': self.context.get('request')}).data
        return data
