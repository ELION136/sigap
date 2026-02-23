"""
Modelos de mantenimiento para el proyecto SIGAP.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.activos.models import Activo
from apps.organizacion.models import Responsable


class TipoMantenimiento(TimeStampedModel):
    """
    Catálogo de tipos de mantenimiento.
    """
    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    color = models.CharField(
        'Color',
        max_length=20,
        default='blue',
        choices=[
            ('green', 'Verde'),
            ('blue', 'Azul'),
            ('yellow', 'Amarillo'),
            ('orange', 'Naranja'),
            ('red', 'Rojo'),
            ('gray', 'Gris'),
            ('purple', 'Morado'),
        ]
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Tipo de Mantenimiento'
        verbose_name_plural = 'Tipos de Mantenimiento'
        ordering = ['codigo', 'nombre']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Mantenimiento(TimeStampedModel):
    """
    Modelo para registrar mantenimientos de activos.
    """
    TIPO_MANTENIMIENTO = [
        ('PREVENTIVO', 'Preventivo'),
        ('CORRECTIVO', 'Correctivo'),
        ('PREDICTIVO', 'Predictivo'),
        ('MEJORA', 'Mejora'),
        ('INSPECCION', 'Inspección'),
        ('CALIBRACION', 'Calibración'),
        ('LIMPIEZA', 'Limpieza'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADO_MANTENIMIENTO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROGRESO', 'En progreso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('POSPUESTO', 'Pospuesto'),
    ]
    
    PRIORIDAD = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    # Relaciones
    activo = models.ForeignKey(
        Activo,
        on_delete=models.CASCADE,
        related_name='mantenimientos',
        verbose_name='Activo'
    )
    tipo = models.CharField(
        'Tipo de mantenimiento',
        max_length=20,
        choices=TIPO_MANTENIMIENTO,
        default='PREVENTIVO'
    )
    
    # Información del mantenimiento
    codigo = models.CharField(
        'Código',
        max_length=50,
        blank=True,
        help_text='Código interno del mantenimiento'
    )
    fecha = models.DateField(
        'Fecha programada'
    )
    fecha_realizacion = models.DateField(
        'Fecha de realización',
        null=True,
        blank=True
    )
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=ESTADO_MANTENIMIENTO,
        default='PENDIENTE'
    )
    prioridad = models.CharField(
        'Prioridad',
        max_length=20,
        choices=PRIORIDAD,
        default='MEDIA'
    )
    
    # Descripción del trabajo
    descripcion = models.TextField(
        'Descripción del trabajo',
        help_text='Descripción detallada del mantenimiento a realizar'
    )
    trabajo_realizado = models.TextField(
        'Trabajo realizado',
        blank=True,
        help_text='Descripción del trabajo efectivamente realizado'
    )
    
    # Personal
    solicitado_por = models.ForeignKey(
        Responsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mantenimientos_solicitados',
        verbose_name='Solicitado por'
    )
    realizado_por = models.ForeignKey(
        Responsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mantenimientos_realizados',
        verbose_name='Realizado por'
    )
    
    # Costos
    costo_mano_obra = models.DecimalField(
        'Costo de mano de obra',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    costo_repuestos = models.DecimalField(
        'Costo de repuestos',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    costo_total = models.DecimalField(
        'Costo total',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    moneda = models.CharField(
        'Moneda',
        max_length=3,
        default='BOB',
        choices=[
            ('BOB', 'Boliviano'),
            ('USD', 'Dólar Americano'),
            ('EUR', 'Euro'),
        ]
    )
    
    # Tiempo
    tiempo_estimado = models.DecimalField(
        'Tiempo estimado (horas)',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    tiempo_real = models.DecimalField(
        'Tiempo real (horas)',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Resultado
    resultado = models.CharField(
        'Resultado',
        max_length=20,
        choices=[
            ('EXITOSO', 'Exitoso'),
            ('PARCIAL', 'Parcial'),
            ('FALLIDO', 'Fallido'),
            ('PENDIENTE', 'Pendiente'),
        ],
        default='PENDIENTE'
    )
    
    # Documentación
    evidencia_fotografica = models.ImageField(
        'Evidencia fotográfica',
        upload_to='mantenimientos/evidencias/',
        blank=True,
        null=True
    )
    documento = models.FileField(
        'Documento adjunto',
        upload_to='mantenimientos/documentos/',
        blank=True,
        null=True
    )
    
    # Notas
    observaciones = models.TextField(
        'Observaciones',
        blank=True
    )
    recomendaciones = models.TextField(
        'Recomendaciones',
        blank=True,
        help_text='Recomendaciones para futuros mantenimientos'
    )
    
    # Próximo mantenimiento
    proximo_mantenimiento = models.DateField(
        'Próximo mantenimiento',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'
        ordering = ['-fecha', '-creado']
        

    def __str__(self):
        return f"{self.codigo or 'MNT-' + str(self.pk)} - {self.activo.nombre}"

    def get_absolute_url(self):
        return reverse('mantenimiento:mantenimiento_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # Calcular costo total
        if self.costo_mano_obra or self.costo_repuestos:
            mano_obra = self.costo_mano_obra or 0
            repuestos = self.costo_repuestos or 0
            self.costo_total = mano_obra + repuestos
        
        super().save(*args, **kwargs)
        
        # Actualizar fechas de mantenimiento en el activo
        if self.estado == 'COMPLETADO' and self.fecha_realizacion:
            self.activo.ultimo_mantenimiento = self.fecha_realizacion
            if self.proximo_mantenimiento:
                self.activo.proximo_mantenimiento = self.proximo_mantenimiento
            elif self.activo.frecuencia_mantenimiento:
                from datetime import timedelta
                self.activo.proximo_mantenimiento = self.fecha_realizacion + timedelta(
                    days=self.activo.frecuencia_mantenimiento
                )
            self.activo.save(update_fields=['ultimo_mantenimiento', 'proximo_mantenimiento'])

    def get_estado_color(self):
        """Retorna el color asociado al estado."""
        colores = {
            'PENDIENTE': 'yellow',
            'EN_PROGRESO': 'blue',
            'COMPLETADO': 'green',
            'CANCELADO': 'gray',
            'POSPUESTO': 'orange',
        }
        return colores.get(self.estado, 'gray')

    def get_prioridad_color(self):
        """Retorna el color asociado a la prioridad."""
        colores = {
            'BAJA': 'green',
            'MEDIA': 'blue',
            'ALTA': 'orange',
            'URGENTE': 'red',
        }
        return colores.get(self.prioridad, 'gray')


class RepuestoUtilizado(TimeStampedModel):
    """
    Modelo para registrar los repuestos utilizados en un mantenimiento.
    """
    mantenimiento = models.ForeignKey(
        Mantenimiento,
        on_delete=models.CASCADE,
        related_name='repuestos',
        verbose_name='Mantenimiento'
    )
    codigo = models.CharField(
        'Código',
        max_length=50,
        blank=True
    )
    descripcion = models.CharField(
        'Descripción',
        max_length=255
    )
    cantidad = models.DecimalField(
        'Cantidad',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    unidad = models.CharField(
        'Unidad',
        max_length=20,
        default='pza',
        choices=[
            ('pza', 'Pieza'),
            ('kg', 'Kilogramo'),
            ('lt', 'Litro'),
            ('m', 'Metro'),
            ('m2', 'Metro cuadrado'),
            ('m3', 'Metro cúbico'),
            ('par', 'Par'),
            ('jgo', 'Juego'),
            ('otro', 'Otro'),
        ]
    )
    costo_unitario = models.DecimalField(
        'Costo unitario',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    costo_total = models.DecimalField(
        'Costo total',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    proveedor = models.CharField(
        'Proveedor',
        max_length=150,
        blank=True
    )
    notas = models.TextField(
        'Notas',
        blank=True
    )

    class Meta:
        verbose_name = 'Repuesto Utilizado'
        verbose_name_plural = 'Repuestos Utilizados'
        ordering = ['descripcion']

    def __str__(self):
        return f"{self.descripcion} ({self.cantidad} {self.unidad})"

    def save(self, *args, **kwargs):
        # Calcular costo total
        if self.costo_unitario and self.cantidad:
            self.costo_total = self.costo_unitario * self.cantidad
        super().save(*args, **kwargs)
