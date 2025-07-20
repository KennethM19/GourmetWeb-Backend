from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_order_receipt_email(user_email, order_data):
    subject = 'Tu boleta de pedido - Gourmet'
    message = render_to_string('emails/order_receipt.txt', {
        'user_name': order_data['user_name'],
        'status': order_data['status'],
        'date_created': order_data['date_created'],
        'total_price': order_data['total_price'],
        'items': order_data['items'],
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False
    )
@shared_task
def test_task():
    return "Test OK"
