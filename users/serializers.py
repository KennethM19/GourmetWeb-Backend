from rest_framework import serializers
from .models import User, Card

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'doc_number', 'first_name', 'last_name', 'phone','email', 'password', 'role', 'date_created')
        read_only_fields = ('date_created', )

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'number', 'cvv', 'date_expired', 'owner', 'is_credit', 'user')