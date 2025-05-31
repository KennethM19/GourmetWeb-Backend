from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from .models import User, Card, Address
from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
    CardCreateSerializer,
    AddressCreateSerializer,
    AddressUpdateSerializer,
    PasswordChangeSerializer
)

# ---------------------- AUTH ----------------------

@api_view(['POST'])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({'message': 'Usuario registrado'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if not check_password(password, user.password):
        return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


# ---------------------- USER ----------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    request.user.delete()
    return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if not check_password(serializer.validated_data['old_password'], user.password):
            return Response({'error': 'Contraseña actual incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Contraseña cambiada correctamente'})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------- CARD ----------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_card(request):
    serializer = CardCreateSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        masked_number = f"**** **** **** {data['number'][-4:]}"

        Card.objects.create(
            number=masked_number,
            date_expired=data['date_expired'],
            owner=data['owner'],
            is_credit=data['is_credit'],
            user=request.user
        )
        return Response({"message": "Tarjeta registrada correctamente."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_card(request, card_id):
    try:
        card = Card.objects.get(id=card_id, user=request.user)
    except Card.DoesNotExist:
        return Response({'error': 'Tarjeta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    card.delete()
    return Response({'message': 'Tarjeta eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


# ---------------------- ADDRESS ----------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_address(request):
    serializer = AddressCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Dirección registrada correctamente."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return Response({'error': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddressUpdateSerializer(address, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
    except Address.DoesNotExist:
        return Response({'error': 'Dirección no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    address.delete()
    return Response({'message': 'Dirección eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)
