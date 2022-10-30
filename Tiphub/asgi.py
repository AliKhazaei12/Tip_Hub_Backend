"""
ASGI config for Tiphub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import Notification.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tiphub.settings')
asgi_application = get_asgi_application()
from channels.routing import ProtocolTypeRouter, URLRouter

import Notification.routing

websocket_urlpatterns = []
websocket_urlpatterns += Notification.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "websocekt": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )

    ),

})
