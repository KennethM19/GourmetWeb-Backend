from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Reservation, ReservationStatus, Table
from .serializers import (
    ReservationSerializer,
    ReservationCreateSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservations(request):
    reservations = Reservation.objects.filter(user=request.user) \
        .select_related('table', 'status')
    serializer = ReservationCreateSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    serializer = ReservationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_data = serializer.validated_data
    people = validated_data['people']
    date = validated_data['date']
    time = validated_data['time']
    phone = validated_data['phone']
    notes = validated_data.get('notes', '')

    candidate_tables = Table.objects.filter(seats__gte=people).order_by('seats')

    for table in candidate_tables:
        ya_reservada = Reservation.objects.filter(table=table, date=date, time=time).exists()
        if not ya_reservada:
            try:
                pending_status = ReservationStatus.objects.get(status__iexact='confirmada')
            except ReservationStatus.DoesNotExist:
                return Response({'error': 'Estado "confirmada" no configurado en la base de datos'}, status=500)

            reservation = Reservation.objects.create(
                user=request.user,
                table=table,
                date=date,
                time=time,
                people=people,
                phone=phone,
                notes=notes,
                status=pending_status
            )

            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

    return Response({'error': 'No hay mesas disponibles para esa cantidad de personas y horario'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservation_by_id(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    cancelled_status = ReservationStatus.objects.filter(status__iexact='cancelada').first()

    if not cancelled_status:
        return Response({'error': 'No se ha configurado el estado "cancelada".'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if reservation.status == cancelled_status:
        return Response({'error': 'La reservación ya fue cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

    reservation.status = cancelled_status
    reservation.save()
    return Response({'message': 'Reservación cancelada correctamente'}, status=status.HTTP_200_OK)
