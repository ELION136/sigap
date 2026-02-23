"""
Signals para la app activos.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Activo, EquipoFuncional, TipoActivo, Estado, TipoPropiedad
from apps.core.models import HistorialCambio


def get_client_info_from_request():
    """Obtiene información del cliente desde el thread local si está disponible."""
    try:
        from django.http import HttpRequest
        # Esto es una simplificación, en producción usar thread local o middleware
        return {'ip': None, 'user_agent': ''}
    except:
        return {'ip': None, 'user_agent': ''}


def serialize_instance(instance):
    """Serializa una instancia de modelo a diccionario."""
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        if value is not None:
            try:
                if hasattr(value, 'pk'):
                    data[field.name] = str(value)
                else:
                    data[field.name] = str(value)
            except:
                data[field.name] = str(value)
    return data


@receiver(post_save, sender=Activo)
def log_activo_save(sender, instance, created, **kwargs):
    """Registra la creación o modificación de un activo."""
    try:
        tipo = 'CREAR' if created else 'MODIFICAR'
        HistorialCambio.registrar(
            tipo_operacion=tipo,
            modelo='Activo',
            objeto_id=instance.pk,
            objeto_repr=str(instance),
            datos_nuevos=serialize_instance(instance)
        )
    except:
        pass


@receiver(post_delete, sender=Activo)
def log_activo_delete(sender, instance, **kwargs):
    """Registra la eliminación de un activo."""
    try:
        HistorialCambio.registrar(
            tipo_operacion='ELIMINAR',
            modelo='Activo',
            objeto_id=instance.pk,
            objeto_repr=str(instance),
            datos_anteriores=serialize_instance(instance)
        )
    except:
        pass


@receiver(post_save, sender=EquipoFuncional)
def log_equipo_save(sender, instance, created, **kwargs):
    """Registra la creación o modificación de un equipo funcional."""
    try:
        tipo = 'CREAR' if created else 'MODIFICAR'
        HistorialCambio.registrar(
            tipo_operacion=tipo,
            modelo='EquipoFuncional',
            objeto_id=instance.pk,
            objeto_repr=str(instance)
        )
    except:
        pass


@receiver(post_delete, sender=EquipoFuncional)
def log_equipo_delete(sender, instance, **kwargs):
    """Registra la eliminación de un equipo funcional."""
    try:
        HistorialCambio.registrar(
            tipo_operacion='ELIMINAR',
            modelo='EquipoFuncional',
            objeto_id=instance.pk,
            objeto_repr=str(instance)
        )
    except:
        pass
