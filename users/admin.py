from django.contrib import admin

from .models import User, Card, Roles, Address

# Register your models here.
admin.site.register(User)
admin.site.register(Card)
admin.site.register(Roles)
admin.site.register(Address)
