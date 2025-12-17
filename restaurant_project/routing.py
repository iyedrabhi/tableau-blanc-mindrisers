from django.urls import re_path
from channels.routing import URLRouter
from reservations import consumers

# Accept with or without trailing slash to avoid 404 from client-side URL variations
websocket_urlpatterns = [
    re_path(r'ws/notifications/?$', consumers.NotificationConsumer.as_asgi()),
]
