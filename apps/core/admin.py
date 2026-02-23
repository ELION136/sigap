"""
Configuración del admin para los modelos de core.
"""
from django.contrib import admin
from .models import HistorialCambio, ConfiguracionSistema


@admin.register(HistorialCambio)
class HistorialCambioAdmin(admin.ModelAdmin):
    list_display = [
        'fecha_hora', 'tipo_operacion', 'modelo', 
        'objeto_repr', 'usuario', 'ip_address'
    ]
    list_filter = ['tipo_operacion', 'modelo', 'fecha_hora']
    search_fields = ['modelo', 'objeto_repr', 'descripcion', 'usuario__username']
    readonly_fields = [
        'fecha_hora', 'usuario', 'tipo_operacion', 'modelo',
        'objeto_id', 'objeto_repr', 'datos_anteriores', 
        'datos_nuevos', 'ip_address', 'user_agent', 'descripcion'
    ]
    date_hierarchy = 'fecha_hora'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['clave', 'valor', 'tipo', 'descripcion', 'editable']
    list_filter = ['tipo', 'editable']
    search_fields = ['clave', 'descripcion']
    readonly_fields = ['creado', 'modificado']
