"""
Modelos de activos para el proyecto SIGAP.
Define los catálogos y modelos principales de activos.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from apps.organizacion.models import Planta, Nivel, Area, SubArea, Responsable


class TipoActivo(TimeStampedModel):
    """
    Catálogo de tipos de activos.
    """
    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True,
        help_text='Código único del tipo de activo'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    categoria = models.CharField(
        'Categoría',
        max_length=50,
        choices=[
            ('MAQUINARIA', 'Maquinaria y Equipo'),
            ('EQUIPO_COMPUTO', 'Equipo de Cómputo'),
            ('MUEBLES', 'Muebles y Enseres'),
            ('EQUIPO_TRANSPORTE', 'Equipo de Transporte'),
            ('EQUIPO_COMUNICACION', 'Equipo de Comunicación'),
            ('HERRAMIENTAS', 'Herramientas'),
            ('INSTALACIONES', 'Instalaciones'),
            ('EDIFICIOS', 'Edificios y Construcciones'),
            ('OTROS', 'Otros'),
        ],
        default='MAQUINARIA'
    )
    vida_util_anios = models.PositiveIntegerField(
        'Vida útil (años)',
        null=True,
        blank=True,
        help_text='Vida útil estimada en años'
    )
    depreciable = models.BooleanField(
        'Depreciable',
        default=True,
        help_text='Indica si el activo de este tipo es depreciable'
    )
    requiere_mantenimiento = models.BooleanField(
        'Requiere mantenimiento',
        default=True,
        help_text='Indica si los activos de este tipo requieren mantenimiento'
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Tipo de Activo'
        verbose_name_plural = 'Tipos de Activos'
        ordering = ['codigo', 'nombre']
        

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('activos:tipoactivo_detail', kwargs={'pk': self.pk})


class Estado(TimeStampedModel):
    """
    Catálogo de estados de activos.
    """
    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True
    )
    nombre = models.CharField(
        'Nombre',
        max_length=50
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    color = models.CharField(
        'Color',
        max_length=20,
        default='gray',
        choices=[
            ('green', 'Verde'),
            ('blue', 'Azul'),
            ('yellow', 'Amarillo'),
            ('orange', 'Naranja'),
            ('red', 'Rojo'),
            ('gray', 'Gris'),
            ('purple', 'Morado'),
        ],
        help_text='Color para identificación visual'
    )
    operativo = models.BooleanField(
        'Operativo',
        default=True,
        help_text='Indica si el activo en este estado puede operar'
    )
    orden = models.PositiveIntegerField(
        'Orden',
        default=0,
        help_text='Orden de visualización'
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['orden', 'nombre']
        

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('activos:estado_detail', kwargs={'pk': self.pk})


class TipoPropiedad(TimeStampedModel):
    """
    Catálogo de tipos de propiedad de activos.
    """
    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True
    )
    nombre = models.CharField(
        'Nombre',
        max_length=50
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Tipo de Propiedad'
        verbose_name_plural = 'Tipos de Propiedad'
        ordering = ['codigo', 'nombre']
        

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('activos:tipopropiedad_detail', kwargs={'pk': self.pk})


class UbicacionActivo(models.Model):
    """
    Modelo para almacenar la ubicación de un activo.
    Permite historial de ubicaciones.
    """
    activo = models.ForeignKey(
        'Activo',
        on_delete=models.CASCADE,
        related_name='ubicaciones',
        verbose_name='Activo'
    )
    planta = models.ForeignKey(
        Planta,
        on_delete=models.PROTECT,
        verbose_name='Planta'
    )
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.PROTECT,
        verbose_name='Nivel'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        verbose_name='Área'
    )
    subarea = models.ForeignKey(
        SubArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Subárea'
    )
    ubicacion_especifica = models.CharField(
        'Ubicación específica',
        max_length=255,
        blank=True,
        help_text='Descripción adicional de la ubicación (ej: Estante A-3, Cuarto 101)'
    )
    fecha_inicio = models.DateTimeField(
        'Fecha de inicio',
        auto_now_add=True
    )
    fecha_fin = models.DateTimeField(
        'Fecha de fin',
        null=True,
        blank=True
    )
    actual = models.BooleanField(
        'Ubicación actual',
        default=True
    )
    observaciones = models.TextField(
        'Observaciones',
        blank=True
    )

    class Meta:
        verbose_name = 'Ubicación de Activo'
        verbose_name_plural = 'Ubicaciones de Activos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        ubicacion = f"{self.planta} > {self.nivel} > {self.area}"
        if self.subarea:
            ubicacion += f" > {self.subarea}"
        return ubicacion


class Activo(TimeStampedModel):
    """
    Modelo principal para la gestión de activos.
    """
    codigo = models.CharField(
        'Código',
        max_length=50,
        unique=True,
        help_text='Código único del activo'
    )
    codigo_interno = models.CharField(
        'Código interno',
        max_length=50,
        blank=True,
        help_text='Código interno de la empresa'
    )
    codigo_contable = models.CharField(
        'Código contable',
        max_length=50,
        blank=True,
        help_text='Código para contabilidad'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=150
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    tipo = models.ForeignKey(
        TipoActivo,
        on_delete=models.PROTECT,
        related_name='activos',
        verbose_name='Tipo de activo'
    )
    estado = models.ForeignKey(
        Estado,
        on_delete=models.PROTECT,
        related_name='activos',
        verbose_name='Estado'
    )
    tipo_propiedad = models.ForeignKey(
        TipoPropiedad,
        on_delete=models.PROTECT,
        related_name='activos',
        verbose_name='Tipo de propiedad'
    )
    
    # Ubicación actual (relación directa para facilitar consultas)
    ubicacion = models.OneToOneField(
        UbicacionActivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activo_principal',
        verbose_name='Ubicación actual'
    )
    
    # Responsable
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activos',
        verbose_name='Responsable'
    )
    
    # Información de compra/adquisición
    fecha_adquisicion = models.DateField(
        'Fecha de adquisición',
        null=True,
        blank=True
    )
    fecha_instalacion = models.DateField(
        'Fecha de instalación',
        null=True,
        blank=True
    )
    fecha_garantia = models.DateField(
        'Fin de garantía',
        null=True,
        blank=True
    )
    proveedor = models.CharField(
        'Proveedor',
        max_length=150,
        blank=True
    )
    numero_factura = models.CharField(
        'Número de factura',
        max_length=50,
        blank=True
    )
    costo_adquisicion = models.DecimalField(
        'Costo de adquisición',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    valor_actual = models.DecimalField(
        'Valor actual',
        max_digits=15,
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
    
    # Especificaciones técnicas
    marca = models.CharField(
        'Marca',
        max_length=100,
        blank=True
    )
    modelo = models.CharField(
        'Modelo',
        max_length=100,
        blank=True
    )
    numero_serie = models.CharField(
        'Número de serie',
        max_length=100,
        blank=True
    )
    capacidad = models.CharField(
        'Capacidad',
        max_length=100,
        blank=True,
        help_text='Capacidad o especificación técnica'
    )
    dimensiones = models.CharField(
        'Dimensiones',
        max_length=100,
        blank=True
    )
    peso = models.DecimalField(
        'Peso (kg)',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Imagen
    imagen = models.ImageField(
        'Imagen',
        upload_to='activos/',
        blank=True,
        null=True
    )
    
    # Documentos
    manual = models.FileField(
        'Manual',
        upload_to='activos/manuales/',
        blank=True,
        null=True
    )
    ficha_tecnica = models.FileField(
        'Ficha técnica',
        upload_to='activos/fichas/',
        blank=True,
        null=True
    )
    
    # Información de mantenimiento
    frecuencia_mantenimiento = models.PositiveIntegerField(
        'Frecuencia de mantenimiento (días)',
        null=True,
        blank=True,
        help_text='Días entre mantenimientos preventivos'
    )
    ultimo_mantenimiento = models.DateField(
        'Último mantenimiento',
        null=True,
        blank=True
    )
    proximo_mantenimiento = models.DateField(
        'Próximo mantenimiento',
        null=True,
        blank=True
    )
    
    # Notas
    notas = models.TextField(
        'Notas',
        blank=True
    )
    
    # Estado del registro
    activo_registro = models.BooleanField(
        'Activo en sistema',
        default=True
    )
    fecha_baja = models.DateField(
        'Fecha de baja',
        null=True,
        blank=True
    )
    motivo_baja = models.TextField(
        'Motivo de baja',
        blank=True
    )

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'
        ordering = ['codigo', 'nombre']
        permissions = [
            ('change_activo_estado', 'Puede cambiar estado de activos'),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('activos:activo_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # Si es nuevo activo, crear ubicación inicial
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.ubicacion:
            self.ubicacion.activo = self
            self.ubicacion.save()

    def get_ubicacion_completa(self):
        """Retorna la ubicación completa como string."""
        if self.ubicacion:
            return str(self.ubicacion)
        return 'Sin ubicación'

    def get_mantenimientos_count(self):
        """Retorna el número de mantenimientos registrados."""
        return self.mantenimientos.count()

    def get_equipos_funcionales(self):
        """Retorna los equipos funcionales a los que pertenece este activo."""
        return self.equipos_funcionales.all()


class EquipoFuncional(TimeStampedModel):
    """
    Modelo para agrupar activos que funcionan como un sistema integral.
    Hereda el responsable de sus activos componentes.
    """
    codigo = models.CharField(
        'Código',
        max_length=50,
        unique=True
    )
    nombre = models.CharField(
        'Nombre',
        max_length=150
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    activos = models.ManyToManyField(
        Activo,
        related_name='equipos_funcionales',
        verbose_name='Activos componentes',
        blank=True
    )
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_funcionales',
        verbose_name='Responsable principal'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name='equipos_funcionales',
        verbose_name='Área'
    )
    estado_operativo = models.CharField(
        'Estado operativo',
        max_length=20,
        choices=[
            ('OPERATIVO', 'Operativo'),
            ('PARCIAL', 'Parcialmente operativo'),
            ('FUERA_SERVICIO', 'Fuera de servicio'),
            ('MANTENIMIENTO', 'En mantenimiento'),
        ],
        default='OPERATIVO'
    )
    criticidad = models.CharField(
        'Criticidad',
        max_length=20,
        choices=[
            ('BAJA', 'Baja'),
            ('MEDIA', 'Media'),
            ('ALTA', 'Alta'),
            ('CRITICA', 'Crítica'),
        ],
        default='MEDIA'
    )
    fecha_instalacion = models.DateField(
        'Fecha de instalación',
        null=True,
        blank=True
    )
    imagen = models.ImageField(
        'Imagen',
        upload_to='equipos/',
        blank=True,
        null=True
    )
    documentacion = models.FileField(
        'Documentación',
        upload_to='equipos/documentos/',
        blank=True,
        null=True
    )
    notas = models.TextField(
        'Notas',
        blank=True
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )

    class Meta:
        verbose_name = 'Equipo Funcional'
        verbose_name_plural = 'Equipos Funcionales'
        ordering = ['codigo', 'nombre']
        

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('activos:equipofuncional_detail', kwargs={'pk': self.pk})

    def get_activos_count(self):
        """Retorna el número de activos en este equipo."""
        return self.activos.count()

    def get_responsable_display(self):
        """Retorna el responsable del equipo o el responsable común de los activos."""
        if self.responsable:
            return self.responsable
        # Buscar responsable común entre los activos
        responsables = self.activos.values_list('responsable', flat=True).distinct()
        if len(responsables) == 1 and responsables[0]:
            return Responsable.objects.get(pk=responsables[0])
        return None

    def actualizar_estado_operativo(self):
        """
        Actualiza el estado operativo del equipo basado en los estados de sus activos.
        """
        activos_count = self.activos.count()
        if activos_count == 0:
            self.estado_operativo = 'FUERA_SERVICIO'
        else:
            activos_operativos = self.activos.filter(estado__operativo=True).count()
            if activos_operativos == activos_count:
                self.estado_operativo = 'OPERATIVO'
            elif activos_operativos == 0:
                self.estado_operativo = 'FUERA_SERVICIO'
            else:
                self.estado_operativo = 'PARCIAL'
        self.save(update_fields=['estado_operativo'])
