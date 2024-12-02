from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from datetime import date

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usuario", null=True)
    nombres = models.CharField(max_length=100, verbose_name=_("Nombres"))
    apellidos = models.CharField(max_length=100, verbose_name=_("Apellidos"))
    email = models.EmailField(unique=True, verbose_name=_("Correo electrónico"))
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message=_("Formato inválido para el número de teléfono."))],
        verbose_name=_("Teléfono"),
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de registro"))
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Nombre de usuario"))
    password = models.CharField(max_length=128, verbose_name=_("Contraseña"))  # Almacena contraseñas en hash
    direccion = models.CharField(max_length=150, blank=True, null=True, verbose_name=_("Dirección"))
    
    tarjeta_numero = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        validators=[
            RegexValidator(r'^\d{16,18}$', message=_("El número de tarjeta debe tener entre 16 y 18 dígitos."))
        ],
        verbose_name=_("Número de tarjeta"),
    )
    tarjeta_cvv = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        validators=[MinLengthValidator(3)],
        verbose_name=_("CVV"),
    )
    tarjeta_fecha_caducidad = models.DateField(
        verbose_name=_("Fecha de caducidad de la tarjeta"),
        help_text=_("Formato: AAAA-MM, debe ser una fecha futura."),
    )
    dni = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^\d{8,12}$', message=_("El DNI debe tener entre 8 y 12 dígitos."))],
        verbose_name=_("DNI"),
    )

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        
        if self.tarjeta_fecha_caducidad and self.tarjeta_fecha_caducidad < date.today():
            raise ValueError(_("La fecha de caducidad de la tarjeta debe ser una fecha futura."))
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.email})"

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ['-fecha_registro']

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=[('plato', 'Plato'), ('bebida', 'Bebida')])
    disponible = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='inventario')
    cantidad_disponible = models.IntegerField(default=0)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventario de {self.producto.nombre}"
    
class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    fecha_reserva = models.DateTimeField()
    numero_personas = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')])
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva para {self.numero_personas} personas el {self.fecha_reserva} por {self.usuario.nombre}"

class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos', blank=True, null=True)
    productos = models.ManyToManyField(Producto, through='PedidoProducto', related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    mesa = models.PositiveIntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('preparación', 'En preparación'), ('servido', 'Servido'), ('cancelado', 'Cancelado')])

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.nombre if self.usuario else 'Usuario sin registro'}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido {self.pedido.id}"

