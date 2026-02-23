# Estructura del Proyecto SIGAP

```
sigap/
├── apps/                           # Aplicaciones Django
│   ├── __init__.py
│   ├── core/                       # Núcleo del sistema
│   │   ├── __init__.py
│   │   ├── admin.py               # Configuración admin
│   │   ├── apps.py                # Configuración app
│   │   ├── context_processors.py  # Procesadores de contexto (menú)
│   │   ├── middleware.py          # Middleware (seguridad, auditoría)
│   │   ├── migrations/
│   │   │   ├── 0001_initial.py    # Migración inicial
│   │   │   └── __init__.py
│   │   ├── models.py              # Modelos: HistorialCambio, ConfiguracionSistema
│   │   ├── signals.py             # Señales para auditoría
│   │   ├── tests.py               # Tests unitarios
│   │   ├── urls.py                # URLs de la app
│   │   ├── utils.py               # Utilidades generales
│   │   └── views.py               # Vistas: Dashboard, Auditoría
│   ├── organizacion/              # Gestión organizacional
│   │   ├── __init__.py
│   │   ├── admin.py               # Configuración admin
│   │   ├── apps.py                # Configuración app
│   │   ├── forms.py               # Formularios
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py              # Modelos: Planta, Nivel, Area, SubArea, Responsable
│   │   ├── urls.py                # URLs de la app
│   │   └── views.py               # Vistas CRUD
│   ├── activos/                   # Gestión de activos
│   │   ├── __init__.py
│   │   ├── admin.py               # Configuración admin
│   │   ├── apps.py                # Configuración app
│   │   ├── forms.py               # Formularios
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py              # Modelos: Activo, EquipoFuncional, Catálogos
│   │   ├── signals.py             # Señales para auditoría
│   │   ├── urls.py                # URLs de la app
│   │   └── views.py               # Vistas CRUD + API AJAX
│   ├── mantenimiento/             # Gestión de mantenimientos
│   │   ├── __init__.py
│   │   ├── admin.py               # Configuración admin
│   │   ├── apps.py                # Configuración app
│   │   ├── forms.py               # Formularios
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py              # Modelos: Mantenimiento, RepuestoUtilizado
│   │   ├── signals.py             # Señales para auditoría
│   │   ├── urls.py                # URLs de la app
│   │   └── views.py               # Vistas CRUD
│   └── reportes/                  # Reportes y exportaciones
│       ├── __init__.py
│       ├── apps.py                # Configuración app
│       ├── urls.py                # URLs de la app
│       └── views.py               # Vistas de reportes y exportaciones
├── config/                        # Configuración del proyecto
│   ├── __init__.py
│   ├── asgi.py                    # Configuración ASGI
│   ├── settings.py                # Configuración principal
│   ├── urls.py                    # URLs principales
│   └── wsgi.py                    # Configuración WSGI
├── certs/                         # Certificados SSL
│   └── .gitkeep
├── docs/                          # Documentación
│   └── INSTALACION.md             # Guía de instalación
├── fixtures/                      # Datos iniciales
│   └── initial_data.json          # Datos de catálogos
├── logs/                          # Archivos de log
│   └── .gitkeep
├── media/                         # Archivos subidos
│   └── .gitkeep
├── scripts/                       # Scripts de utilidad
│   ├── quickstart.sh              # Script de inicio rápido
│   └── setup_groups.py            # Configuración de grupos
├── static/                        # Archivos estáticos (desarrollo)
├── staticfiles/                   # Archivos estáticos (producción)
├── templates/                     # Plantillas HTML
│   ├── base.html                  # Plantilla base
│   ├── core/
│   │   └── dashboard.html         # Dashboard principal
│   ├── includes/
│   │   ├── footer.html            # Footer
│   │   ├── header.html            # Header
│   │   └── sidebar.html           # Barra lateral navegable
│   ├── organizacion/
│   │   ├── planta_detail.html     # Detalle de planta
│   │   ├── planta_form.html       # Formulario de planta
│   │   └── planta_list.html       # Lista de plantas
│   └── registration/
│       └── login.html             # Página de login
├── .env.example                   # Ejemplo de variables de entorno
├── .gitignore                     # Archivos ignorados por git
├── ESTRUCTURA.md                  # Este archivo
├── gunicorn.conf.py               # Configuración de Gunicorn
├── manage.py                      # Script de gestión Django
├── README.md                      # Documentación principal
└── requirements.txt               # Dependencias Python
```

## Modelos Principales

### Core
- **HistorialCambio**: Registro de auditoría de todas las operaciones
- **ConfiguracionSistema**: Configuraciones del sistema

### Organización
- **Planta**: Instalación industrial
- **Nivel**: Piso o nivel dentro de una planta
- **Area**: Área funcional
- **SubArea**: Subdivisión de área
- **Responsable**: Persona responsable

### Activos
- **TipoActivo**: Catálogo de tipos de activos
- **Estado**: Catálogo de estados
- **TipoPropiedad**: Catálogo de tipos de propiedad
- **UbicacionActivo**: Historial de ubicaciones
- **Activo**: Bien mueble o equipo
- **EquipoFuncional**: Agrupación de activos

### Mantenimiento
- **TipoMantenimiento**: Catálogo de tipos de mantenimiento
- **Mantenimiento**: Registro de mantenimiento
- **RepuestoUtilizado**: Piezas y materiales utilizados

## URLs Principales

| URL | Descripción |
|-----|-------------|
| `/` | Dashboard |
| `/admin/` | Panel de administración |
| `/accounts/login/` | Inicio de sesión |
| `/organizacion/` | Gestión organizacional |
| `/activos/` | Gestión de activos |
| `/mantenimiento/` | Gestión de mantenimientos |
| `/reportes/` | Reportes y exportaciones |
| `/auditoria/` | Historial de auditoría |

## Permisos por Rol

### Administrador
- Acceso total al sistema

### Encargado de Área
- view_activo, add_activo, change_activo
- view_equipofuncional, add_equipofuncional, change_equipofuncional
- view_mantenimiento, add_mantenimiento, change_mantenimiento

### Operador
- view_activo, change_activo_estado
- view_mantenimiento, add_mantenimiento

### Consulta
- Solo permisos de vista (view_*)
