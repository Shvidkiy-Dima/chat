from rest_framework.routers import SimpleRouter
from .views import DialogViewSet

router = SimpleRouter()
router.register('dialog', DialogViewSet)

urlpatterns = router.urls
