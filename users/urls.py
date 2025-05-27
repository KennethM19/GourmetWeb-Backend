from rest_framework import routers

from .views import UserViewSet, CardViewSet, RolesViewSet, register_user

router = routers.DefaultRouter()

router.register('api/users', UserViewSet, 'users')
router.register('api/cards', CardViewSet, 'cards')
router.register('api/roles', RolesViewSet, 'roles')

urlpatterns = router.urls