from django.urls import path

from .views import get_reservations, get_reservation_by_id, create_reservation, cancel_reservation

urlpatterns = [
    path('get/', get_reservations, name='get_reservations'),
    path('create/', create_reservation, name='create_reservation'),
    path('<int:reservation_id>/', get_reservation_by_id, name='get_reservation_by_id'),
    path('<int:reservation_id>/cancel/', cancel_reservation, name='cancel_reservation'),
]
