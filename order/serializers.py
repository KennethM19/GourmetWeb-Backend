from operator import itemgetter

from rest_framework import serializers
from .models import Product, ProductType, Order, OrderItem, OrderStatus
from users.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------------- PRODUCT ----------------------

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    productType = ProductTypeSerializer()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# ---------------------- ORDER ----------------------

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.FloatField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'product_price', 'quantity']

class OrderItemCreateSerializer(serializers.ModelSerializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status = serializers.CharField(source='status.status')
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'status', 'date_created', 'total_price', 'items']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        order.update_total_price()
        return order