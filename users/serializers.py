from rest_framework import serializers
from .models import User, Card, Roles

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'role']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = self.hash_password(raw_password)
        user.save()
        return user

    def hash_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        return make_password(raw_password)

class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['id', 'date_created']

class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['number', 'date_expired', 'owner', 'is_credit']

    def validate_number(self, value):
        if not value.isdigit() or len(value) < 13 or len(value) > 19:
            raise serializers.ValidationError("Número de tarjeta inválido.")
        return value

class CardSerializer(serializers.ModelSerializer):
    last_four_digits = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id', 'last_four_digits', 'date_expired', 'owner', 'is_credit']

    def get_last_four_digits(self, obj):
        return obj.number[-4:]

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'