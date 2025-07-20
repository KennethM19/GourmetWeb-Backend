from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import get_products, get_product_by_id, create_product, update_product, delete_product, get_orders, \
    get_order_by_id, create_order, delete_order, get_product_types, create_product_type, list_orders, \
    change_order_status

urlpatterns = [
                  path('products/', get_products, name='get_products'),
                  path('products/create/', create_product, name='create_product'),
                  path('products/<int:product_id>/', get_product_by_id, name='get_product_by_id'),
                  path('products/<int:product_id>/update/', update_product, name='update_product'),
                  path('products/<int:product_id>/delete/', delete_product, name='delete_product'),
                  path('get/', get_orders, name='get_orders'),
                  path('create/', create_order, name='create_order'),
                  path('<int:order_id>/', get_order_by_id, name='get_order_by_id'),
                  path('<int:order_id>/delete/', delete_order, name='delete_order'),
                  path('product-types/', get_product_types, name='get_product_types'),
                  path('product-types/create/', create_product_type, name='create_product_type'),
                  path('orders-list/', list_orders, name='list_orders'),
                  path('<int:order_id>/change-status/', change_order_status, name='cook_change_order_status'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
