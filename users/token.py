from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        try:
            user = User.objects.get(**{self.username_field: attrs[self.username_field]})
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail':'Usuario no existe'})

        if not check_password(attrs['password'], user.password):
            raise serializers.ValidationError({'detail':'Contraseña incorrecta'})

        data = super().get_token(user)
        return {
            'access_token': str(data.access_token),
            'refresh_token': str(data),
        }