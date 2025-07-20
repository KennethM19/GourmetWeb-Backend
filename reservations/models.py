from django.conf import settings
from django.db import models


class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Mesa {self.number} ({self.seats} asientos)"


class ReservationStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservation')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    time = models.TimeField()
    people = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)
    status = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE, related_name='reservations', default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('table', 'date', 'time')

    def __str__(self):
        return f"Reserva de {self.user} - Mesa {self.table.number} el {self.date} a las {self.time}"
