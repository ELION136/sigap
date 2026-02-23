"""
Configuración del admin para la app activos.
"""
from django.contrib import admin
from .models import (
    TipoActivo, Estado, TipoPropiedad, 
    Activo, UbicacionActivo, EquipoFuncional
)


class UbicacionActivoInline(admin.TabularInline):
    model = UbicacionActivo
    extra = 0
    readonly_fields = ['fecha_inicio']


@admin.register(TipoActivo)
class TipoActivoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'categoria', 'vida_util_anios',
        'depreciable', 'requiere_mantenimiento', 'activo'
    ]
    list_filter = ['categoria', 'depreciable', 'requiere_mantenimiento', 'activo']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['orden', 'codigo', 'nombre', 'color', 'operativo', 'activo']
    list_editable = ['orden']
    list_display_links = ['codigo', 'nombre']  # Agregar esta línea
    list_filter = ['operativo', 'activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']


@admin.register(TipoPropiedad)
class TipoPropiedadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo']
    search_fields = ['codigo', 'nombre']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']


@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'tipo', 'estado', 'tipo_propiedad',
        'responsable', 'activo_registro'
    ]
    list_filter = [
        'tipo', 'estado', 'tipo_propiedad', 
        'activo_registro', 'tipo__categoria'
    ]
    search_fields = [
        'codigo', 'nombre', 'descripcion', 
        'numero_serie', 'marca', 'modelo'
    ]
    readonly_fields = [
        'creado', 'modificado', 'creado_por', 'modificado_por',
        'ultimo_mantenimiento', 'proximo_mantenimiento'
    ]
    #filter_horizontal = ['equipos_funcionales']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'codigo_interno', 'codigo_contable', 'nombre', 'descripcion')
        }),
        ('Clasificación', {
            'fields': ('tipo', 'estado', 'tipo_propiedad')
        }),
        ('Ubicación y Responsable', {
            'fields': ('ubicacion', 'responsable')
        }),
        ('Adquisición', {
            'fields': (
                'fecha_adquisicion', 'fecha_instalacion', 'fecha_garantia',
                'proveedor', 'numero_factura', 'costo_adquisicion',
                'valor_actual', 'moneda'
            )
        }),
        ('Especificaciones Técnicas', {
            'fields': ('marca', 'modelo', 'numero_serie', 'capacidad', 'dimensiones', 'peso'),
            'classes': ('collapse',)
        }),
        ('Archivos', {
            'fields': ('imagen', 'manual', 'ficha_tecnica'),
            'classes': ('collapse',)
        }),
        ('Mantenimiento', {
            'fields': ('frecuencia_mantenimiento', 'ultimo_mantenimiento', 'proximo_mantenimiento'),
            'classes': ('collapse',)
        }),
        ('Estado del Registro', {
            'fields': ('activo_registro', 'fecha_baja', 'motivo_baja', 'notas'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('creado', 'modificado', 'creado_por', 'modificado_por'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EquipoFuncional)
class EquipoFuncionalAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'area', 'responsable',
        'estado_operativo', 'criticidad', 'activo'
    ]
    list_filter = ['estado_operativo', 'criticidad', 'activo', 'area__nivel__planta']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']
    filter_horizontal = ['activos']
