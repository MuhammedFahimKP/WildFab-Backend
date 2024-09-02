"""
ASGI config for ecom project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from accounts.routing import websocket_urlpatterns


from accounts.middlewars import PathAuthMiddleware


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')




# 👇 1. Update the below import lib


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 👇 2. Update the application var
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            PathAuthMiddleware(URLRouter(
                websocket_urlpatterns
            ))
        ),
})