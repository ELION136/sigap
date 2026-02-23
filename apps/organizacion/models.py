"""
Modelos de organización para el proyecto SIGAP.
Define la estructura jerárquica: Planta > Nivel > Área > Subárea
"""
from django.db import models
from django.urls import reverse
from apps.core.models import TimeStampedModel


class Planta(TimeStampedModel):
    """
    Modelo que representa una planta industrial o instalación.
    Es el nivel más alto de la jerarquía organizacional.
    """
    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True,
        help_text='Código único de la planta (ej: PLT-001)'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100,
        help_text='Nombre de la planta'
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True,
        help_text='Descripción detallada de la planta'
    )
    direccion = models.CharField(
        'Dirección',
        max_length=255,
        blank=True
    )
    ciudad = models.CharField(
        'Ciudad',
        max_length=100,
        blank=True
    )
    estado_provincia = models.CharField(
        'Estado/Provincia',
        max_length=100,
        blank=True
    )
    codigo_postal = models.CharField(
        'Código Postal',
        max_length=20,
        blank=True
    )
    pais = models.CharField(
        'País',
        max_length=100,
        default='México'
    )
    telefono = models.CharField(
        'Teléfono',
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        'Correo electrónico',
        blank=True
    )
    latitud = models.DecimalField(
        'Latitud',
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True
    )
    longitud = models.DecimalField(
        'Longitud',
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True
    )
    activa = models.BooleanField(
        'Activa',
        default=True,
        help_text='Indica si la planta está activa'
    )
    imagen = models.ImageField(
        'Imagen',
        upload_to='plantas/',
        blank=True,
        null=True,
        help_text='Imagen o foto de la planta'
    )

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'
        ordering = ['codigo', 'nombre']
        

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('organizacion:planta_detail', kwargs={'pk': self.pk})

    def get_niveles_count(self):
        """Retorna el número de niveles en esta planta."""
        return self.niveles.count()

    def get_areas_count(self):
        """Retorna el número de áreas en esta planta."""
        return Area.objects.filter(nivel__planta=self).count()


class Nivel(TimeStampedModel):
    """
    Modelo que representa un nivel o piso dentro de una planta.
    """
    planta = models.ForeignKey(
        Planta,
        on_delete=models.CASCADE,
        related_name='niveles',
        verbose_name='Planta'
    )
    codigo = models.CharField(
        'Código',
        max_length=20,
        help_text='Código del nivel (ej: N1, PISO-1)'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100,
        help_text='Nombre descriptivo del nivel'
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    numero_nivel = models.IntegerField(
        'Número de nivel',
        default=0,
        help_text='Número del nivel (0 = planta baja, negativos = sótanos)'
    )
    altura = models.DecimalField(
        'Altura (m)',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Altura del nivel en metros'
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )
    plano = models.ImageField(
        'Plano',
        upload_to='planos/niveles/',
        blank=True,
        null=True,
        help_text='Plano arquitectónico del nivel'
    )

    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
        ordering = ['planta', 'numero_nivel', 'codigo']
        unique_together = ['planta', 'codigo']
        

    def __str__(self):
        return f"{self.planta.codigo} - {self.codigo}: {self.nombre}"

    def get_absolute_url(self):
        return reverse('organizacion:nivel_detail', kwargs={'pk': self.pk})

    def get_areas_count(self):
        """Retorna el número de áreas en este nivel."""
        return self.areas.count()


class Area(TimeStampedModel):
    """
    Modelo que representa un área funcional dentro de un nivel.
    """
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        related_name='areas',
        verbose_name='Nivel'
    )
    codigo = models.CharField(
        'Código',
        max_length=20,
        help_text='Código del área (ej: PROD-01, MANT)'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    tipo_area = models.CharField(
        'Tipo de área',
        max_length=50,
        choices=[
            ('PRODUCCION', 'Producción'),
            ('ALMACEN', 'Almacén'),
            ('MANTENIMIENTO', 'Mantenimiento'),
            ('CALIDAD', 'Calidad'),
            ('LABORATORIO', 'Laboratorio'),
            ('OFICINA', 'Oficina'),
            ('SEGURIDAD', 'Seguridad'),
            ('LOGISTICA', 'Logística'),
            ('OTRO', 'Otro'),
        ],
        default='PRODUCCION'
    )
    supervisor = models.ForeignKey(
        'Responsable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='areas_supervisadas',
        verbose_name='Supervisor'
    )
    activa = models.BooleanField(
        'Activa',
        default=True
    )
    plano = models.ImageField(
        'Plano',
        upload_to='planos/areas/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['nivel__planta', 'nivel', 'codigo']
        unique_together = ['nivel', 'codigo']
        

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('organizacion:area_detail', kwargs={'pk': self.pk})

    @property
    def planta(self):
        """Retorna la planta a la que pertenece esta área."""
        return self.nivel.planta

    def get_subareas_count(self):
        """Retorna el número de subáreas en esta área."""
        return self.subareas.count()

    def get_activos_count(self):
        """Retorna el número de activos en esta área."""
        from apps.activos.models import Activo
        return Activo.objects.filter(ubicacion__area=self).count()


class SubArea(TimeStampedModel):
    """
    Modelo que representa una subárea o sección dentro de un área.
    Es el nivel más granular de la jerarquía organizacional.
    """
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='subareas',
        verbose_name='Área'
    )
    codigo = models.CharField(
        'Código',
        max_length=20,
        help_text='Código de la subárea'
    )
    nombre = models.CharField(
        'Nombre',
        max_length=100
    )
    descripcion = models.TextField(
        'Descripción',
        blank=True
    )
    responsable = models.ForeignKey(
        'Responsable',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subareas_responsable',
        verbose_name='Responsable'
    )
    activa = models.BooleanField(
        'Activa',
        default=True
    )

    class Meta:
        verbose_name = 'Subárea'
        verbose_name_plural = 'Subáreas'
        ordering = ['area', 'codigo']
        unique_together = ['area', 'codigo']
        

    def __str__(self):
        return f"{self.area.codigo}.{self.codigo} - {self.nombre}"

    def get_absolute_url(self):
        return reverse('organizacion:subarea_detail', kwargs={'pk': self.pk})

    @property
    def nivel(self):
        """Retorna el nivel al que pertenece esta subárea."""
        return self.area.nivel

    @property
    def planta(self):
        """Retorna la planta a la que pertenece esta subárea."""
        return self.area.nivel.planta


class Responsable(TimeStampedModel):
    """
    Modelo que representa a una persona responsable de activos o áreas.
    """
    TIPO_RESPONSABLE = [
        ('INTERNO', 'Interno'),
        ('EXTERNO', 'Externo'),
        ('CONTRATISTA', 'Contratista'),
    ]

    codigo = models.CharField(
        'Código',
        max_length=20,
        unique=True,
        help_text='Código único del responsable'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=20,
        choices=TIPO_RESPONSABLE,
        default='INTERNO'
    )
    nombres = models.CharField(
        'Nombres',
        max_length=100
    )
    apellidos = models.CharField(
        'Apellidos',
        max_length=100
    )
    puesto = models.CharField(
        'Puesto',
        max_length=100,
        blank=True
    )
    departamento = models.CharField(
        'Departamento',
        max_length=100,
        blank=True
    )
    email = models.EmailField(
        'Correo electrónico',
        blank=True
    )
    telefono = models.CharField(
        'Teléfono',
        max_length=50,
        blank=True
    )
    telefono_movil = models.CharField(
        'Teléfono móvil',
        max_length=50,
        blank=True
    )
    direccion = models.TextField(
        'Dirección',
        blank=True
    )
    fecha_ingreso = models.DateField(
        'Fecha de ingreso',
        null=True,
        blank=True
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )
    notas = models.TextField(
        'Notas',
        blank=True
    )
    foto = models.ImageField(
        'Foto',
        upload_to='responsables/',
        blank=True,
        null=True
    )
    # Relación opcional con usuario del sistema
    usuario = models.OneToOneField(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsable',
        verbose_name='Usuario del sistema'
    )

    class Meta:
        verbose_name = 'Responsable'
        verbose_name_plural = 'Responsables'
        ordering = ['apellidos', 'nombres']
        

    def __str__(self):
        return f"{self.codigo} - {self.apellidos}, {self.nombres}"

    def get_absolute_url(self):
        return reverse('organizacion:responsable_detail', kwargs={'pk': self.pk})

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del responsable."""
        return f"{self.nombres} {self.apellidos}"

    def get_activos_count(self):
        """Retorna el número de activos asignados a este responsable."""
        from apps.activos.models import Activo
        return Activo.objects.filter(responsable=self).count()

    def get_equipos_count(self):
        """Retorna el número de equipos funcionales asignados a este responsable."""
        from apps.activos.models import EquipoFuncional
        return EquipoFuncional.objects.filter(responsable=self).count()
