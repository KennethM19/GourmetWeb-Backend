from django.urls import path
from .views import get_products, get_product_by_id, create_product, update_product, delete_product, get_orders, get_order_by_id, create_order, delete_order, get_product_types, create_product_type

urlpatterns = [
    path('products/', get_products, name='get_products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
    path('products/<int:product_id>/update/', update_product, name='update_product'),
    path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
    path('orders/', get_orders, name='get_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('orders/<int:order_id>/', get_order_by_id, name='get_order_by_id'),
    path('orders/<int:order_id>/delete/', delete_order, name='delete_order'),
    path('product-types/', get_product_types, name='get_product_types'),
    path('product-types/create/', create_product_type, name='create_product_type'),
]