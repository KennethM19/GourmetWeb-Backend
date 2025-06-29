from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


# Create your models here.
class Roles(models.Model):
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.role

class User(AbstractBaseUser, PermissionsMixin):
    doc_number = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                   message="Formato inválido para el número de teléfono.")],
        verbose_name="Phone"
    )
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey('Roles', on_delete=models.CASCADE, default=1, related_name='user')
    date_created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Campo usado para login
    REQUIRED_FIELDS = ['first_name', 'last_name', 'doc_number']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Card(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cards')
    number = models.CharField(max_length=100)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    owner = models.CharField(max_length=100)
    is_credit = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if len(self.number) > 4:
            self.number = self.number[-4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number}, {self.owner}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, blank=True, null=True)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.street}, {self.city}"