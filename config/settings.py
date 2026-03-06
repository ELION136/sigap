"""
Configuración de Django para el proyecto SIGAP - Sistema Integral de Gestión de Activos de Planta.

Para más información sobre este archivo, ver:
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de environ
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    SECURE_SSL_REDIRECT=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),
)

# Lee el archivo .env si existe
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# =============================================================================
# CONFIGURACIÓN BÁSICA
# =============================================================================

SECRET_KEY = env('SECRET_KEY', default='django-insecure-cambiar-en-produccion-sigap-2024')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Aplicaciones de Django
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

# Aplicaciones de terceros
THIRD_PARTY_APPS = [
    'crispy_forms',
    'crispy_tailwind',
    'django_filters',
    'django_tables2',
    'django_extensions',
]

# Aplicaciones locales
LOCAL_APPS = [
    'apps.core',
    'apps.organizacion',
    'apps.activos',
    'apps.mantenimiento',
    'apps.reportes',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.AuditLogMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.menu_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =============================================================================
# BASE DE DATOS
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='sigap_db'),
        'USER': env('DB_USER', default='sigap_user'),
        'PASSWORD': env('DB_PASSWORD', default='sigap_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# =============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# =============================================================================
# INTERNACIONALIZACIÓN
# =============================================================================

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# =============================================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# =============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# CONFIGURACIÓN DE CRISPY FORMS
# =============================================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# =============================================================================
# CONFIGURACIÓN DE DJANGO-TABLES2
# =============================================================================

DJANGO_TABLES2_TEMPLATE = "django_tables2/tailwind.html"

# =============================================================================
# SEGURIDAD (Configuración para HTTPS en intranet)
# =============================================================================

# Solo habilitar en producción con HTTPS
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuración de sesiones
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 28800  # 8 horas

# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'sigap.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# =============================================================================
# CONFIGURACIÓN DE PAGINACIÓN
# =============================================================================

PAGINATE_BY = 25

# =============================================================================
# CONFIGURACIÓN DE SUBIDA DE ARCHIVOS
# =============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

# Tipos de imagen permitidos
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB



# =============================================================================
# AUTENTICACIÓN Y REDIRECCIONES
# =============================================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'login'


# =============================================================================
# DEFAULT PRIMARY KEY
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CONFIGURACIÓN DE RED LOCAL (INTRANET)
# =============================================================================

# Fuerza el uso de la aplicación solo en red local
# Descomentar en producción para restringir acceso
# INTERNAL_IPS = ['127.0.0.1', '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']

# =============================================================================
# CONFIGURACIÓN DE ROLES Y PERMISOS PERSONALIZADOS
# =============================================================================

# Grupos de usuarios predefinidos
GROUPS = {
    'Administrador': {
        'permissions': '__all__',
        'description': 'Acceso total al sistema'
    },
    'Encargado de Área': {
        'permissions': [
            'view_activo', 'add_activo', 'change_activo',
            'view_equipofuncional', 'add_equipofuncional', 'change_equipofuncional',
            'view_mantenimiento', 'add_mantenimiento', 'change_mantenimiento',
        ],
        'description': 'Gestión de activos en su área asignada'
    },
    'Operador': {
        'permissions': [
            'view_activo', 'change_activo_estado',
            'view_mantenimiento', 'add_mantenimiento',
        ],
        'description': 'Cambios de estado y registro de mantenimientos'
    },
    'Consulta': {
        'permissions': [
            'view_activo', 'view_equipofuncional',
            'view_mantenimiento', 'view_historialcambio',
        ],
        'description': 'Solo lectura de información'
    },
}
