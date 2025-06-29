from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Order, ProductType, OrderStatus
from .serializers import ProductSerializer, ProductCreateSerializer, OrderSerializer, OrderCreateSerializer, ProductTypeSerializer

# Create your views here.

# ---------------------- PRODUCT ----------------------

@api_view(['GET'])
def get_products(request):
    products = Product.objects.select_related('productType').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def create_product(request):
    serializer = ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_product_by_id(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])  # Solo admin/staff puede editar
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductCreateSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Solo admin/staff puede eliminar
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAdminUser])  # Solo admins pueden crear tipos
def create_product_type(request):
    serializer = ProductTypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_product_types(request):
    types = ProductType.objects.all()
    serializer = ProductTypeSerializer(types, many=True)
    return Response(serializer.data)

# ---------------------- ORDER ----------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user).select_related('status').prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if order.status.status.lower() != "pendiente" and str(request.user.role).lower() == 'cliente':
        return Response({'error': 'Solo puedes eliminar órdenes pendientes'}, status=status.HTTP_400_BAD_REQUEST)

    order.delete()
    return Response({'message': 'Orden eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    # Solo usuarios con rol 'cocina' pueden acceder
    if str(request.user.role).lower() != 'cocina':
        return Response({'detail': 'Solo cocineros pueden acceder a esta vista'}, status=status.HTTP_403_FORBIDDEN)

    status_param = request.query_params.get('status')  # Captura ?status=Pendiente

    if status_param:
        status_obj = OrderStatus.objects.filter(status__iexact=status_param).first()
        if not status_obj:
            return Response({'detail': f'No existe el estado "{status_param}"'}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(status=status_obj)
    else:
        orders = Order.objects.all()

    # Optimizar queries
    orders = orders.select_related('status', 'user').prefetch_related('items__product')

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_order_status(request, order_id):
    if str(request.user.role) != 'cocina':
        return Response({'detail': 'Solo cocineros pueden cambiar el estado de las órdenes'}, status=status.HTTP_403_FORBIDDEN)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'detail': 'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    status_id = request.data.get('status_id')
    if not status_id:
        return Response({'detail': 'Se requiere "status_id"'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        new_status = OrderStatus.objects.get(id=status_id)
    except OrderStatus.DoesNotExist:
        return Response({'detail': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save()
    return Response({'message': f'Estado actualizado a {new_status.status}'}, status=status.HTTP_200_OK)