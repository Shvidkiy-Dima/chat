from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DialogViewSet, MessageViewSet

dialog_router = SimpleRouter()
message_router = SimpleRouter()
dialog_router.register('dialog', DialogViewSet)
message_router.register('message', MessageViewSet)

urlpatterns = [
    path('dialog/<int:dialog>/', include(message_router.urls)),
    path('', include(dialog_router.urls)),
]
