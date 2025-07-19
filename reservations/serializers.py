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
    table = TableSerializer()
    status = ReservationStatusSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'table', 'date', 'time', 'status', 'created_at']

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time']

    def validate(self, data):
        table = data['table']
        date = data['date']
        time = data['time']

        if Reservation.objects.filter(table=table, date=date, time=time).exists():
            raise serializers.ValidationError('La mesa ya está reservada en ese horario.')

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return Reservation.objects.create(user=user, **validated_data)

