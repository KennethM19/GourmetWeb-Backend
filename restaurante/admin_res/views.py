from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import Http404
from .models import Usuario, Producto, Inventario, Reserva, Pedido, PedidoProducto
from .serializers import *

@permission_classes([AllowAny])
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer  
    
    def destroy(self, request, *args, **kwargs):
        try:
            try:
                instance = self.get_object()
            except Http404:
                raise NotFound("El usuario que intenta eliminar no existe.")

            with transaction.atomic():
                user = getattr(instance, 'user', None)
                if user:
                    try:
                        user.delete()
                    except Exception as user_delete_error:
                        raise ValidationError(
                            {"auth_user": f"Error al eliminar el usuario en auth_user: {str(user_delete_error)}"}
                        )
                else:
                    raise NotFound("El usuario asociado no existe o ya ha sido eliminado.")

                try:
                    instance.delete()
                except Exception as instance_delete_error:
                    raise ValidationError(
                        {"usuario": f"Error al eliminar el registro en Usuario: {str(instance_delete_error)}"}
                    )

                return Response({"message": "Usuario eliminado con éxito."}, status=status.HTTP_200_OK)

        except NotFound as nf_error:
            return Response({"error": str(nf_error)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve_error:
            return Response(ve_error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as general_error:
            return Response(
                {"error": f"Ha ocurrido un error inesperado: {str(general_error)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer  # Solo hay un serializer para Producto

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InventarioWriteSerializer
        return InventarioReadSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReservaWriteSerializer
        return ReservaReadSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PedidoWriteSerializer
        return PedidoReadSerializer

class PedidoProductoViewSet(viewsets.ModelViewSet):
    queryset = PedidoProducto.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PedidoProductoWriteSerializer
        return PedidoProductoReadSerializer
