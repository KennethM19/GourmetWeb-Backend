from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_reservation_email(email, name, date, time, table_number):
    subject = 'Confirmación de tu reservación - GourmetWeb'
    message = (
        f'Hola {name},\n\n'
        f'Tu reservación ha sido confirmada para el día {date} a las {time}.\n'
        f'Mesa asignada: {table_number}.\n\n'
        f'¡Gracias por elegirnos!\n\n'
        f'- El equipo de GourmetWeb'
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
@shared_task
def test_task():
    return "Test OK"
