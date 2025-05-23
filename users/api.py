from .models import User, Card
from rest_framework import viewsets, permissions

from .serializers import UserSerializer, CardSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CardSerializer