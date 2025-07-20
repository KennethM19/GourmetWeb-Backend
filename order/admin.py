from django.contrib import admin

from order.models import Order, Product, OrderItem, OrderStatus, ProductType

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)
admin.site.register(ProductType)
