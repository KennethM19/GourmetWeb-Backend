from rest_framework import serializers

from .models import Reservation, Table, ReservationStatus


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'seats']


class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStatus
        fields = ['id', 'status']


class ReservationSerializer(serializers.ModelSerializer):
    table = serializers.IntegerField(source='table.number')
    status = serializers.CharField(source='status.status')

    class Meta:
        model = Reservation
        fields = ['id', 'table', 'date', 'time', 'status', 'created_at']


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'date', 'time', 'people', 'phone', 'notes', 'table', 'status', 'created_at']
        read_only_fields = ['table', 'status', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        return Reservation.objects.create(user=user, **validated_data)
