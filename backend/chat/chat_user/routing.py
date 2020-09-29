from rest_framework.routers import SimpleRouter
from .views import ChatUserViewSet

router = SimpleRouter()
router.register('users', ChatUserViewSet)

urlpatterns = router.urls