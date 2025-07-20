from django.contrib import admin

from reservations.models import Table, ReservationStatus, Reservation

# Register your models here.
admin.site.register(Table)
admin.site.register(ReservationStatus)
admin.site.register(Reservation)