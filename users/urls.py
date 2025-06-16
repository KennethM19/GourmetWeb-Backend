from django.urls import path
from .views import (
    register, login, get_user, update_user, delete_user, change_password,
    get_cards, register_card, delete_card,
    get_addresses, register_address, update_address, delete_address
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Autenticación
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Usuario
    path('profile/', get_user, name='get_user'),
    path('profile/update/', update_user, name='update_user'),
    path('profile/delete/', delete_user, name='delete_user'),
    path('profile/change-password/', change_password, name='change_password'),

    # Tarjetas
    path('cards/', get_cards, name='get_cards'),
    path('cards/register/', register_card, name='register_card'),
    path('cards/<int:card_id>/delete/', delete_card, name='delete_card'),

    # Direcciones
    path('addresses/', get_addresses, name='get_addresses'),
    path('addresses/register/', register_address, name='register_address'),
    path('addresses/<int:address_id>/update/', update_address, name='update_address'),
    path('addresses/<int:address_id>/delete/', delete_address, name='delete_address'),
]
