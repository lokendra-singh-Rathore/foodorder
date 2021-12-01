"""
ASGI config for foodapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from django.core.asgi import get_asgi_application
from django.urls import path
from home  import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodapp.settings')

application = get_asgi_application()


ws_pattern= [
    path('ws/pizza/<order_id>',consumers.OrderProgress.as_asgi()),
]

application= ProtocolTypeRouter(
    {
        'websocket':AuthMiddlewareStack(URLRouter(ws_pattern))
    }
)

