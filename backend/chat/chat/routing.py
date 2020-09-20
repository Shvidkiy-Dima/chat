from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from communication.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {'websocket': AllowedHostsOriginValidator(
            URLRouter(websocket_urlpatterns)
    )
    }
)