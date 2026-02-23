#!/usr/bin/env python
"""
Script para configurar los grupos y permisos iniciales del sistema SIGAP.
Ejecutar con: python manage.py shell < scripts/setup_groups.py
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_groups():
    """Crea los grupos de usuarios del sistema."""
    groups = {
        'Administrador': {
            'description': 'Acceso total al sistema',
            'permissions': '__all__'
        },
        'Encargado de Área': {
            'description': 'Gestión de activos en su área asignada',
            'permissions': [
                # Activos
                'view_activo', 'add_activo', 'change_activo',
                'view_equipofuncional', 'add_equipofuncional', 'change_equipofuncional',
                # Mantenimiento
                'view_mantenimiento', 'add_mantenimiento', 'change_mantenimiento',
                # Organización (solo lectura)
                'view_planta', 'view_nivel', 'view_area', 'view_subarea', 'view_responsable',
                # Reportes
                'view_reporte',
            ]
        },
        'Operador': {
            'description': 'Cambios de estado y registro de mantenimientos',
            'permissions': [
                # Activos (solo lectura y cambio de estado)
                'view_activo', 'change_activo_estado',
                # Mantenimiento
                'view_mantenimiento', 'add_mantenimiento',
                # Equipos (solo lectura)
                'view_equipofuncional',
                # Organización (solo lectura)
                'view_planta', 'view_nivel', 'view_area', 'view_subarea', 'view_responsable',
            ]
        },
        'Consulta': {
            'description': 'Solo lectura de información',
            'permissions': [
                # Solo permisos de vista
                'view_activo', 'view_equipofuncional',
                'view_mantenimiento', 'view_historialcambio',
                'view_planta', 'view_nivel', 'view_area', 'view_subarea', 'view_responsable',
                'view_tipoactivo', 'view_estado', 'view_tipopropiedad',
                'view_tipomantenimiento', 'view_repuestoutilizado',
                'view_reporte',
            ]
        },
    }
    
    for group_name, config in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        
        if created:
            print(f"Grupo '{group_name}' creado exitosamente.")
        else:
            print(f"Grupo '{group_name}' ya existe.")
        
        # Asignar permisos
        if config['permissions'] == '__all__':
            # Administrador: todos los permisos
            all_permissions = Permission.objects.all()
            group.permissions.set(all_permissions)
            print(f"  -> Todos los permisos asignados.")
        else:
            # Otros roles: permisos específicos
            permissions = Permission.objects.filter(codename__in=config['permissions'])
            group.permissions.set(permissions)
            print(f"  -> {permissions.count()} permisos asignados.")
    
    print("\nConfiguración de grupos completada.")


if __name__ == '__main__':
    create_groups()
