"""
Signals para el proyecto SIGAP.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.contenttypes.models import ContentType
from .models import HistorialCambio
import json


def get_client_info(request):
    """Obtiene información del cliente desde la request."""
    if request:
        return {
            'ip': getattr(request, 'audit_ip', None),
            'user_agent': getattr(request, 'audit_user_agent', '')
        }
    return {'ip': None, 'user_agent': ''}


def serialize_instance(instance):
    """Serializa una instancia de modelo a diccionario."""
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if value is not None:
            try:
                # Intentar serializar el valor
                if hasattr(value, 'pk'):
                    data[field.name] = str(value)
                else:
                    data[field.name] = str(value)
            except:
                data[field.name] = str(value)
    return data


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Registra el inicio de sesión de usuarios."""
    client_info = get_client_info(request)
    HistorialCambio.registrar(
        tipo_operacion='LOGIN',
        modelo='User',
        objeto_id=user.pk,
        objeto_repr=f'Usuario: {user.username}',
        usuario=user,
        ip_address=client_info['ip'],
        user_agent=client_info['user_agent'],
        descripcion=f'Inicio de sesión: {user.username}'
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Registra el cierre de sesión de usuarios."""
    if user:
        client_info = get_client_info(request)
        HistorialCambio.registrar(
            tipo_operacion='LOGOUT',
            modelo='User',
            objeto_id=user.pk,
            objeto_repr=f'Usuario: {user.username}',
            usuario=user,
            ip_address=client_info['ip'],
            user_agent=client_info['user_agent'],
            descripcion=f'Cierre de sesión: {user.username}'
        )
