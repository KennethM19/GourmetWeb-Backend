from django.conf import settings
from django.db import models
from django.db.models import Sum, F


# Create your models here.
class ProductType(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type


class Product(models.Model):
    productType = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='productImages/', blank=True, null=True)
    available = models.BooleanField(default=True)
    cant_available = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    status = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.status}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        total = self.items.aggregate(
            total=Sum(F('quantity') * F('product__price')))['total'] or 0
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} de {self.user}, {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en pedido {self.order.id}"
