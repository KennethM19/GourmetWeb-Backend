from rest_framework import serializers
from .models import User, Card, Roles

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('date_created', )

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = self.hash_password(raw_password)
        user.save()
        return user

    def hash_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        return make_password(raw_password)

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'