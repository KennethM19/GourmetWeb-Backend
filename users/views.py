# Create your views here.
from .models import User, Card
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserSerializer, CardSerializer, CardCreateSerializer

@api_view(['POST'])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
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
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_card(request):
    cards = Card.objects.filter(user=request.user)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_card(request):
    serializer = CardCreateSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data

        last_four = validated_data['number'][-4:]
        masked_number = f"**** **** **** {last_four}"

        card = Card.objects.create(
            number=masked_number,
            date_expired=validated_data['date_expired'],
            owner=validated_data['owner'],
            is_credit=validated_data['is_credit'],
            user=request.user
        )
        return Response({"message": "Tarjeta registrada correctamente."}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)