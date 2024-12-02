from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedidos-productos', PedidoProductoViewSet)

url_api = [
    path('api/v1/login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

url_api_secundario = [
]

urlpatterns = url_api_secundario + url_api +[
    path('api/v1/', include(router.urls)),
]