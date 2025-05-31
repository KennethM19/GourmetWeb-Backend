from django.urls import path
from .views import register, get_user, login, get_card, register_card
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('get-user/', get_user, name='user'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-card/', get_card, name='get_card'),
    path('register-card/', register_card, name='register-card'),
]