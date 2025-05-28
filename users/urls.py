from django.urls import path
from .views import register, users, login
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', users, name='users'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]