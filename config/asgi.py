"""
Configuración ASGI para el proyecto SIGAP.

Expone la variable de aplicación ASGI como un módulo-level llamado ``application``.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
