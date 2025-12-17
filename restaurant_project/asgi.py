"""
ASGI config for restaurant_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_project.settings')

# Simple ASGI application using Django's ASGI application.
# We removed Channels support; this file now exposes the standard
# Django ASGI app so deployment (if desired) can still use ASGI.
application = get_asgi_application()
