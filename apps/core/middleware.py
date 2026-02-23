"""
Middleware para el proyecto SIGAP.
"""
import logging
from .models import HistorialCambio

logger = logging.getLogger('apps')


class AuditLogMiddleware:
    """
    Middleware que captura la IP y User-Agent del usuario para auditoría.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código antes de la vista
        if request.user.is_authenticated:
            request.audit_ip = self.get_client_ip(request)
            request.audit_user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        response = self.get_response(request)
        
        return response

    def get_client_ip(self, request):
        """
        Obtiene la IP real del cliente, considerando proxies.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware:
    """
    Middleware que agrega headers de seguridad a las respuestas.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
