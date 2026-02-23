"""
Configuración del admin para la app organizacion.
"""
from django.contrib import admin
from .models import Planta, Nivel, Area, SubArea, Responsable


class NivelInline(admin.TabularInline):
    model = Nivel
    extra = 0
    fields = ['codigo', 'nombre', 'numero_nivel', 'activo']


@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'ciudad', 'estado_provincia', 
        'activa', 'creado'
    ]
    list_filter = ['activa', 'estado_provincia', 'pais']
    search_fields = ['codigo', 'nombre', 'direccion']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']
    fieldsets = (
        ('Información General', {
            'fields': ('codigo', 'nombre', 'descripcion', 'activa')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad', 'estado_provincia', 'codigo_postal', 'pais')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email')
        }),
        ('Coordenadas', {
            'fields': ('latitud', 'longitud'),
            'classes': ('collapse',)
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Auditoría', {
            'fields': ('creado', 'modificado', 'creado_por', 'modificado_por'),
            'classes': ('collapse',)
        }),
    )
    inlines = [NivelInline]


class AreaInline(admin.TabularInline):
    model = Area
    extra = 0
    fields = ['codigo', 'nombre', 'tipo_area', 'activa']


@admin.register(Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'planta', 'numero_nivel', 'activo'
    ]
    list_filter = ['planta', 'activo']
    search_fields = ['codigo', 'nombre', 'planta__nombre']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']
    inlines = [AreaInline]


class SubAreaInline(admin.TabularInline):
    model = SubArea
    extra = 0
    fields = ['codigo', 'nombre', 'responsable', 'activa']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'nivel', 'tipo_area', 'supervisor', 'activa'
    ]
    list_filter = ['tipo_area', 'activa', 'nivel__planta']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']
    inlines = [SubAreaInline]


@admin.register(SubArea)
class SubAreaAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nombre', 'area', 'responsable', 'activa'
    ]
    list_filter = ['activa', 'area__nivel__planta']
    search_fields = ['codigo', 'nombre', 'area__nombre']
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']


@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'apellidos', 'nombres', 'puesto', 'tipo', 'activo'
    ]
    list_filter = ['tipo', 'activo']
    search_fields = [
        'codigo', 'nombres', 'apellidos', 
        'email', 'telefono', 'puesto'
    ]
    readonly_fields = ['creado', 'modificado', 'creado_por', 'modificado_por']
    fieldsets = (
        ('Información Personal', {
            'fields': ('codigo', 'tipo', 'nombres', 'apellidos', 'foto')
        }),
        ('Información Laboral', {
            'fields': ('puesto', 'departamento', 'fecha_ingreso')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'telefono_movil', 'direccion')
        }),
        ('Sistema', {
            'fields': ('usuario', 'activo')
        }),
        ('Notas', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('creado', 'modificado', 'creado_por', 'modificado_por'),
            'classes': ('collapse',)
        }),
    )
