"""
Modelos base y de auditoría para el proyecto SIGAP.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
import json


User = get_user_model()


class TimeStampedModel(models.Model):
    """
    Modelo abstracto que proporciona campos de fecha de creación y modificación.
    """
    creado = models.DateTimeField(
        'Fecha de creación',
        auto_now_add=True,
        help_text='Fecha y hora en que se creó el registro'
    )
    modificado = models.DateTimeField(
        'Fecha de modificación',
        auto_now=True,
        help_text='Fecha y hora de la última modificación'
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_creado_por',
        verbose_name='Creado por'
    )
    modificado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_modificado_por',
        verbose_name='Modificado por'
    )

    class Meta:
        abstract = True


class HistorialCambio(models.Model):
    """
    Modelo para registrar todos los cambios realizados en el sistema.
    Implementa auditoría completa de operaciones CRUD.
    """
    TIPO_OPERACION = [
        ('CREAR', 'Creación'),
        ('MODIFICAR', 'Modificación'),
        ('ELIMINAR', 'Eliminación'),
        ('CONSULTAR', 'Consulta'),
        ('ESTADO', 'Cambio de Estado'),
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
    ]

    fecha_hora = models.DateTimeField(
        'Fecha y hora',
        auto_now_add=True,
        help_text='Fecha y hora del cambio'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
        help_text='Usuario que realizó la operación'
    )
    tipo_operacion = models.CharField(
        'Tipo de operación',
        max_length=20,
        choices=TIPO_OPERACION,
        help_text='Tipo de operación realizada'
    )
    modelo = models.CharField(
        'Modelo afectado',
        max_length=100,
        help_text='Nombre del modelo que fue modificado'
    )
    objeto_id = models.CharField(
        'ID del objeto',
        max_length=50,
        help_text='Identificador del objeto afectado'
    )
    objeto_repr = models.CharField(
        'Representación del objeto',
        max_length=255,
        blank=True,
        help_text='Representación legible del objeto'
    )
    datos_anteriores = models.JSONField(
        'Datos anteriores',
        null=True,
        blank=True,
        help_text='Datos del objeto antes del cambio (JSON)'
    )
    datos_nuevos = models.JSONField(
        'Datos nuevos',
        null=True,
        blank=True,
        help_text='Datos del objeto después del cambio (JSON)'
    )
    ip_address = models.GenericIPAddressField(
        'Dirección IP',
        null=True,
        blank=True,
        help_text='Dirección IP desde donde se realizó la operación'
    )
    user_agent = models.TextField(
        'User Agent',
        blank=True,
        help_text='Información del navegador/cliente'
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True,
        help_text='Descripción adicional del cambio'
    )

    class Meta:
        verbose_name = 'Historial de Cambio'
        verbose_name_plural = 'Historial de Cambios'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['-fecha_hora']),
            models.Index(fields=['modelo', 'tipo_operacion']),
            models.Index(fields=['usuario']),
        ]
        

    def __str__(self):
        return f"{self.get_tipo_operacion_display()} - {self.modelo} ({self.fecha_hora.strftime('%Y-%m-%d %H:%M')})"

    @classmethod
    def registrar(cls, tipo_operacion, modelo, objeto_id, objeto_repr='', 
                  datos_anteriores=None, datos_nuevos=None, usuario=None,
                  ip_address=None, user_agent=None, descripcion=''):
        """
        Método de clase para registrar un cambio en el historial.
        """
        return cls.objects.create(
            tipo_operacion=tipo_operacion,
            modelo=modelo,
            objeto_id=str(objeto_id),
            objeto_repr=objeto_repr[:255],
            datos_anteriores=datos_anteriores,
            datos_nuevos=datos_nuevos,
            usuario=usuario,
            ip_address=ip_address,
            user_agent=user_agent[:500] if user_agent else '',
            descripcion=descripcion
        )


class ConfiguracionSistema(models.Model):
    """
    Modelo para almacenar configuraciones del sistema.
    """
    clave = models.CharField(
        'Clave',
        max_length=100,
        unique=True,
        help_text='Identificador único de la configuración'
    )
    valor = models.TextField(
        'Valor',
        help_text='Valor de la configuración'
    )
    descripcion = models.CharField(
        'Descripción',
        max_length=255,
        blank=True
    )
    tipo = models.CharField(
        'Tipo de dato',
        max_length=20,
        choices=[
            ('string', 'Texto'),
            ('int', 'Entero'),
            ('float', 'Decimal'),
            ('bool', 'Booleano'),
            ('json', 'JSON'),
        ],
        default='string'
    )
    editable = models.BooleanField(
        'Editable',
        default=True,
        help_text='Si puede ser modificado desde la interfaz'
    )
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración del Sistema'
        verbose_name_plural = 'Configuraciones del Sistema'
        ordering = ['clave']

    def __str__(self):
        return self.clave

    def get_valor(self):
        """
        Retorna el valor convertido al tipo de dato correspondiente.
        """
        if self.tipo == 'int':
            return int(self.valor)
        elif self.tipo == 'float':
            return float(self.valor)
        elif self.tipo == 'bool':
            return self.valor.lower() in ('true', '1', 'yes', 'si')
        elif self.tipo == 'json':
            return json.loads(self.valor)
        return self.valor
