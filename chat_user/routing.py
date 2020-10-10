from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ChatUserViewSet

router = SimpleRouter()
router.register('users', ChatUserViewSet)

urlpatterns = [path('login/', include('rest_social_auth.urls_jwt_pair')),
               *router.urls]
