from rest_framework import routers

from .api import UserViewSet, CardViewSet

router = routers.DefaultRouter()

router.register('api/users', UserViewSet, 'users')
router.register('api/cards', CardViewSet, 'cards')

urlpatterns = router.urls