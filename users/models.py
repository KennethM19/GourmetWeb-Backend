from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Roles(models.Model):
    role = models.CharField(max_length=100)

class User(models.Model):
    doc_number = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15,
                             blank=True,
                             null=True,
                             validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                                        message="Formato inválido para el número de teléfono.")],
                             verbose_name="Phone"
                             )
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    cvv = models.CharField(max_length=100)
    date_expired = models.DateTimeField(null=True)
    owner = models.CharField(max_length=100)
    is_credit = models.BooleanField(default=False)