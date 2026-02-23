"""
Context processors para el proyecto SIGAP.
"""
from django.urls import reverse
from django.contrib.auth.models import Permission


def menu_context(request):
    """
    Context processor que proporciona el menú de navegación según permisos.
    """
    if not request.user.is_authenticated:
        return {'menu_items': []}
    
    user = request.user
    menu_items = []
    
    # Dashboard - disponible para todos los usuarios autenticados
    menu_items.append({
        'name': 'Dashboard',
        'icon': 'home',
        'url': reverse('core:dashboard'),
        'active': request.path == reverse('core:dashboard'),
        'submenu': []
    })
    
    # Organización
    if user.has_perm('organizacion.view_planta') or user.is_superuser:
        org_submenu = []
        if user.has_perm('organizacion.view_planta') or user.is_superuser:
            org_submenu.append({
                'name': 'Plantas',
                'url': reverse('organizacion:planta_list'),
                'active': 'planta' in request.path
            })
            org_submenu.append({
                'name': 'Niveles',
                'url': reverse('organizacion:nivel_list'),
                'active': 'nivel' in request.path
            })
            org_submenu.append({
                'name': 'Áreas',
                'url': reverse('organizacion:area_list'),
                'active': 'area' in request.path
            })
            org_submenu.append({
                'name': 'Subáreas',
                'url': reverse('organizacion:subarea_list'),
                'active': 'subarea' in request.path
            })
        if user.has_perm('organizacion.view_responsable') or user.is_superuser:
            org_submenu.append({
                'name': 'Responsables',
                'url': reverse('organizacion:responsable_list'),
                'active': 'responsable' in request.path
            })
        
        menu_items.append({
            'name': 'Organización',
            'icon': 'building',
            'url': '#',
            'active': 'organizacion' in request.path,
            'submenu': org_submenu
        })
    
    # Activos
    if user.has_perm('activos.view_activo') or user.is_superuser:
        activo_submenu = [
            {
                'name': 'Activos',
                'url': reverse('activos:activo_list'),
                'active': 'activo' in request.path and 'tipo' not in request.path and 'estado' not in request.path and 'propiedad' not in request.path
            },
            {
                'name': 'Equipos Funcionales',
                'url': reverse('activos:equipofuncional_list'),
                'active': 'equipofuncional' in request.path
            },
        ]
        
        # Catálogos solo para administradores
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            activo_submenu.extend([
                {
                    'name': 'Tipos de Activo',
                    'url': reverse('activos:tipoactivo_list'),
                    'active': 'tipoactivo' in request.path
                },
                {
                    'name': 'Estados',
                    'url': reverse('activos:estado_list'),
                    'active': 'estado' in request.path and 'activo' in request.path
                },
                {
                    'name': 'Tipos de Propiedad',
                    'url': reverse('activos:tipopropiedad_list'),
                    'active': 'tipopropiedad' in request.path
                },
            ])
        
        menu_items.append({
            'name': 'Activos',
            'icon': 'box',
            'url': '#',
            'active': 'activos' in request.path,
            'submenu': activo_submenu
        })
    
    # Mantenimiento
    if user.has_perm('mantenimiento.view_mantenimiento') or user.is_superuser:
        menu_items.append({
            'name': 'Mantenimiento',
            'icon': 'tools',
            'url': reverse('mantenimiento:mantenimiento_list'),
            'active': 'mantenimiento' in request.path,
            'submenu': []
        })
    
    # Reportes
    if user.has_perm('reportes.view_reporte') or user.is_superuser:
        menu_items.append({
            'name': 'Reportes',
            'icon': 'chart-bar',
            'url': reverse('reportes:index'),
            'active': 'reportes' in request.path,
            'submenu': []
        })
    
    # Historial (solo administradores)
    if user.is_superuser or user.groups.filter(name='Administrador').exists():
        menu_items.append({
            'name': 'Auditoría',
            'icon': 'history',
            'url': reverse('core:auditoria_list'),
            'active': 'auditoria' in request.path,
            'submenu': []
        })
    
    return {'menu_items': menu_items}
