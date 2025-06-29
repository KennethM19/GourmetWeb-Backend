from rest_framework import serializers
from .models import User, Card, Address

# ---------------------- CARD ----------------------

class CardCreateSerializer(serializers.ModelSerializer):
    is_credit = serializers.BooleanField(default=False)

    class Meta:
        model = Card
        fields = ['number', 'exp_month', 'exp_year', 'owner', 'is_credit']

    def validate_number(self, value):
        if not value.isdigit() or len(value) < 13 or len(value) > 19:
            raise serializers.ValidationError("Número de tarjeta inválido.")
        return value

    def validate_exp_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("El mes debe estar entre 1 y 12.")
        return value

    def validate_exp_year(self, value):
        if value < 2024:
            raise serializers.ValidationError("El año debe ser igual o mayor al actual.")
        return value

class CardSerializer(serializers.ModelSerializer):
    last_four_digits = serializers.SerializerMethodField()
    expiration = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id', 'last_four_digits', 'expiration', 'owner', 'is_credit']

    def get_last_four_digits(self, obj):
        return obj.number[-4:]

    def get_expiration(self, obj):
        return f"{obj.exp_month:02d}/{obj.exp_year % 100}"

# ---------------------- ADDRESS ----------------------

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

# ---------------------- USER ----------------------

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['doc_number','email', 'password', 'first_name', 'last_name', 'phone', 'role']

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
    addresses = AddressSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['id']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)