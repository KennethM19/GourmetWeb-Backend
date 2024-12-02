from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Extraer datos para el usuario
                username = validated_data.get("username", None) or validated_data["email"]
                email = validated_data["email"]
                password = validated_data["password"]
                first_name = validated_data.get("nombres")
                last_name = validated_data.get("apellidos")

                # Crear el usuario en auth_user
                try:
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                except Exception as user_error:
                    raise ValidationError({"auth_user": f"Error al crear el usuario: {user_error}"})

                # Crear el usuario en el modelo Usuario
                try:
                    usuario = Usuario.objects.create(user=user, **validated_data)
                except Exception as usuario_error:
                    raise ValidationError({"usuario": f"Error al crear el usuario personalizado: {usuario_error}"})

                return usuario

        except ValidationError as ve:
            # Permite que los errores de validación sean manejados por DRF
            raise ve
        except Exception as general_error:
            # Captura cualquier otro error inesperado
            raise ValidationError({"general": f"Error inesperado: {general_error}"})
                 
    def update(self, instance, validated_data):
        with transaction.atomic():
            # Actualizar el usuario
            instance.nombres = validated_data.get("nombres", instance.nombres)
            instance.apellidos = validated_data.get("apellidos", instance.apellidos)
            instance.email = validated_data.get("email", instance.email)
            instance.telefono = validated_data.get("telefono", instance.telefono)
            instance.direccion = validated_data.get("direccion", instance.direccion)
            instance.tarjeta_numero = validated_data.get("tarjeta_numero", instance.tarjeta_numero)
            instance.tarjeta_cvv = validated_data.get("tarjeta_cvv", instance.tarjeta_cvv)
            instance.tarjeta_fecha_caducidad = validated_data.get("tarjeta_fecha_caducidad", instance.tarjeta_fecha_caducidad)
            instance.dni = validated_data.get("dni", instance.dni)

            # Actualizar la contraseña si es necesario
            password = validated_data.get("password", None)
            if password and not password.startswith('pbkdf2_sha256$'):
                instance.password = make_password(password)

            # Guardar los cambios en el usuario
            instance.save()

            # Actualizar el usuario asociado en auth_user
            user = instance.user
            if user:
                user.username = validated_data.get("username", user.username)
                user.email = validated_data.get("email", user.email)
                user.first_name = validated_data.get("nombres", user.first_name)
                user.last_name = validated_data.get("apellidos", user.last_name)
                if password:
                    user.set_password(password)
                user.save()

            return instance   

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class InventarioReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only = True)

    class Meta:
        model = Inventario
        fields = '__all__'

class InventarioWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        fields = '__all__'

class ReservaReadSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only = True)

    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class PedidoProductoReadSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only = True)

    class Meta:
        model = PedidoProducto
        fields = '__all__'

class PedidoProductoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoProducto
        fields = '__all__'

class PedidoReadSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only = True)
    productos = PedidoProductoReadSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoWriteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    productos = PedidoProductoWriteSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'

