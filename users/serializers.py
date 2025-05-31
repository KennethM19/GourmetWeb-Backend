from rest_framework import serializers
from .models import User, Card, Address

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

class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'number', 'apartment', 'district', 'city', 'zip_code']

class AddressSerializer(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['full_address']

    def get_full_address(self, obj):
        return f"{obj.street} - {obj.number}, {obj.district}, {obj.city}"

class AddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'number', 'apartment', 'district', 'city', 'zip_code']

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
    addresses = AddressSerializer(source='address_set', many=True, read_only=True)
    cards = CardSerializer(source='card_set', many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['id', 'date_created']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)