from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Inventario)
admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)