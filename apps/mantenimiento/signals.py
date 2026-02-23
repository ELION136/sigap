"""
Signals para la app mantenimiento.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mantenimiento, RepuestoUtilizado
from apps.core.models import HistorialCambio


@receiver(post_save, sender=Mantenimiento)
def log_mantenimiento_save(sender, instance, created, **kwargs):
    """Registra la creación o modificación de un mantenimiento."""
    try:
        tipo = 'CREAR' if created else 'MODIFICAR'
        HistorialCambio.registrar(
            tipo_operacion=tipo,
            modelo='Mantenimiento',
            objeto_id=instance.pk,
            objeto_repr=str(instance),
            descripcion=f'{instance.get_tipo_display()} - {instance.activo}'
        )
    except:
        pass


@receiver(post_delete, sender=Mantenimiento)
def log_mantenimiento_delete(sender, instance, **kwargs):
    """Registra la eliminación de un mantenimiento."""
    try:
        HistorialCambio.registrar(
            tipo_operacion='ELIMINAR',
            modelo='Mantenimiento',
            objeto_id=instance.pk,
            objeto_repr=str(instance)
        )
    except:
        pass
