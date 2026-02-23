"""
Configuración WSGI para el proyecto SIGAP.

Expone la variable de aplicación WSGI como un módulo-level llamado ``application``.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
