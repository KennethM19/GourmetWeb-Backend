from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Reservation, ReservationStatus
from .serializers import (
    ReservationSerializer,
    ReservationCreateSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)\
        .select_related('table', 'status')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reservation(request):
    serializer = ReservationCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        reservation = serializer.save()
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'error': 'No se ha configurado el estado "cancelada".'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if reservation.status == cancelled_status:
        return Response({'error': 'La reservación ya fue cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

    reservation.status = cancelled_status
    reservation.save()
    return Response({'message': 'Reservación cancelada correctamente'}, status=status.HTTP_200_OK)
