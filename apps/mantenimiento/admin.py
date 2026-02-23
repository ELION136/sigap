"""
Configuración del admin para la app mantenimiento.
"""
from django.contrib import admin
from .models import TipoMantenimiento, Mantenimiento, RepuestoUtilizado


class RepuestoUtilizadoInline(admin.TabularInline):
    model = RepuestoUtilizado
    extra = 1
    fields = ['codigo', 'descripcion', 'cantidad', 'unidad', 'costo_unitario', 'costo_total']
    readonly_fields = ['costo_total']


@admin.register(TipoMantenimiento)
class TipoMantenimientoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'color', 'activo']
    list_filter = ['activo']
    search_fields = ['codigo', 'nombre']


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'activo', 'tipo', 'fecha', 'estado', 
        'prioridad', 'resultado', 'costo_total'
    ]
    list_filter = [
        'tipo', 'estado', 'prioridad', 'resultado',
        'fecha', 'activo__tipo'
    ]
    search_fields = [
        'codigo', 'activo__nombre', 'activo__codigo',
        'descripcion', 'trabajo_realizado'
    ]
    readonly_fields = [
        'creado', 'modificado', 'creado_por', 'modificado_por',
        'costo_total'
    ]
    date_hierarchy = 'fecha'
    inlines = [RepuestoUtilizadoInline]
    fieldsets = (
        ('Información General', {
            'fields': ('activo', 'tipo', 'codigo', 'fecha', 'estado', 'prioridad')
        }),
        ('Descripción del Trabajo', {
            'fields': ('descripcion', 'trabajo_realizado')
        }),
        ('Personal', {
            'fields': ('solicitado_por', 'realizado_por')
        }),
        ('Costos', {
            'fields': ('costo_mano_obra', 'costo_repuestos', 'costo_total', 'moneda')
        }),
        ('Tiempo', {
            'fields': ('tiempo_estimado', 'tiempo_real', 'fecha_realizacion')
        }),
        ('Resultado', {
            'fields': ('resultado', 'proximo_mantenimiento')
        }),
        ('Documentación', {
            'fields': ('evidencia_fotografica', 'documento'),
            'classes': ('collapse',)
        }),
        ('Notas', {
            'fields': ('observaciones', 'recomendaciones'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('creado', 'modificado', 'creado_por', 'modificado_por'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RepuestoUtilizado)
class RepuestoUtilizadoAdmin(admin.ModelAdmin):
    list_display = [
        'descripcion', 'mantenimiento', 'cantidad', 
        'unidad', 'costo_unitario', 'costo_total'
    ]
    list_filter = ['unidad']
    search_fields = ['descripcion', 'codigo', 'mantenimiento__codigo']
    readonly_fields = ['costo_total']
