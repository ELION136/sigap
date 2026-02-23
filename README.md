# SIGAP - Sistema Integral de Gestión de Activos de Planta

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0-38B2AC.svg)](https://tailwindcss.com/)

Sistema web integral para la gestión, control y seguimiento de activos de planta industrial. Desarrollado con Django 5, PostgreSQL y Tailwind CSS.

## Características Principales

### Gestión Organizacional
- **Jerarquía completa**: Planta > Nivel > Área > Subárea
- **Responsables**: Asignación de responsables por área y activo
- **Ubicación precisa**: Seguimiento de ubicación de cada activo

### Gestión de Activos
- **Código único**: Identificación única para cada activo
- **Clasificación**: Por tipo, estado y tipo de propiedad
- **Especificaciones técnicas**: Marca, modelo, número de serie, capacidad
- **Imágenes y documentos**: Soporte para fotos, manuales y fichas técnicas
- **Historial de ubicaciones**: Seguimiento de movimientos

### Equipos Funcionales
- **Agrupación de activos**: Crear equipos funcionales con múltiples activos
- **Herencia de responsable**: El equipo hereda el responsable de sus componentes
- **Estado operativo**: Seguimiento del estado del equipo completo

### Mantenimientos
- **Tipos de mantenimiento**: Preventivo, correctivo, predictivo, calibración
- **Programación**: Fechas de mantenimiento programadas
- **Costos**: Registro de costos de mano de obra y repuestos
- **Repuestos utilizados**: Detalle de piezas y materiales
- **Evidencias**: Fotos y documentos adjuntos

### Control y Auditoría
- **Historial de cambios**: Registro automático de todas las operaciones
- **Trazabilidad**: Quién, cuándo y qué cambió
- **IP y User-Agent**: Información de sesión para auditoría

### Reportes y Exportaciones
- **Dashboard**: Resumen visual con estadísticas
- **Reportes filtrables**: Por fecha, tipo, estado, ubicación
- **Exportación Excel**: Datos de activos y mantenimientos

### Seguridad y Permisos
- **Roles predefinidos**:
  - Administrador: Acceso total
  - Encargado de Área: Gestión en su área
  - Operador: Cambios de estado y mantenimientos
  - Consulta: Solo lectura
- **HTTPS**: Soporte para certificados SSL autofirmados
- **Protección CSRF**: Seguridad en formularios

## Arquitectura del Sistema

```
SIGAP/
├── apps/
│   ├── core/           # Modelos base, auditoría, utilidades
│   ├── organizacion/   # Planta, Nivel, Área, Subárea, Responsable
│   ├── activos/        # Activos, Equipos Funcionales, Catálogos
│   ├── mantenimiento/  # Mantenimientos, Repuestos
│   └── reportes/       # Reportes y exportaciones
├── config/             # Configuración de Django
├── fixtures/           # Datos iniciales
├── media/              # Archivos subidos
├── static/             # Archivos estáticos
├── templates/          # Plantillas HTML
└── docs/               # Documentación
```

## Modelos Principales

| Modelo | Descripción |
|--------|-------------|
| `Planta` | Instalación industrial principal |
| `Nivel` | Piso o nivel dentro de una planta |
| `Area` | Área funcional dentro de un nivel |
| `SubArea` | Subdivisión de un área |
| `Responsable` | Persona responsable de activos |
| `Activo` | Bien mueble o equipo a gestionar |
| `EquipoFuncional` | Agrupación de activos relacionados |
| `Mantenimiento` | Registro de mantenimiento |
| `HistorialCambio` | Auditoría de operaciones |

## Tecnologías Utilizadas

- **Backend**: Django 5.0, Python 3.10+
- **Base de Datos**: PostgreSQL 13+
- **Frontend**: Tailwind CSS, Alpine.js
- **Formularios**: Django Crispy Forms
- **Tablas**: Django Tables 2
- **Exportación**: OpenPyXL (Excel)

## Instalación Rápida

```bash
# 1. Clonar repositorio
git clone <url-repositorio>
cd sigap

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos PostgreSQL
# Ver docs/INSTALACION.md para detalles

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con los valores apropiados

# 6. Ejecutar migraciones
python manage.py migrate

# 7. Cargar datos iniciales
python manage.py loaddata fixtures/initial_data.json

# 8. Configurar grupos y permisos
python manage.py shell < scripts/setup_groups.py

# 9. Crear superusuario
python manage.py createsuperuser

# 10. Iniciar servidor
python manage.py runserver
```

Para una instalación completa en producción, consulte [docs/INSTALACION.md](docs/INSTALACION.md).

## Uso del Sistema

### Acceso

1. Abrir navegador y acceder a `http://localhost:8000`
2. Iniciar sesión con credenciales de administrador
3. El dashboard muestra resumen de activos y alertas

### Flujo de Trabajo Típico

1. **Configurar Organización**
   - Crear Planta(s)
   - Definir Niveles
   - Crear Áreas y Subáreas
   - Registrar Responsables

2. **Registrar Activos**
   - Crear activos con código único
   - Asignar ubicación y responsable
   - Subir imágenes y documentos

3. **Crear Equipos Funcionales**
   - Agrupar activos relacionados
   - Asignar responsable al equipo

4. **Programar Mantenimientos**
   - Crear mantenimientos preventivos
   - Registrar mantenimientos correctivos
   - Documentar repuestos utilizados

5. **Generar Reportes**
   - Consultar activos por filtros
   - Exportar a Excel
   - Revisar historial de auditoría

## Configuración de Roles

### Administrador
- Acceso completo al sistema
- Gestión de usuarios y permisos
- Configuración del sistema

### Encargado de Área
- Gestión de activos en su área
- Creación de mantenimientos
- Reportes de su área

### Operador
- Cambios de estado de activos
- Registro de mantenimientos
- Consulta de información

### Consulta
- Solo lectura de información
- Generación de reportes
- Sin permisos de modificación

## Seguridad

### Configuración HTTPS

El sistema está diseñado para funcionar en red local con HTTPS:

```bash
# Generar certificado autofirmado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/sigap.key \
    -out certs/sigap.crt
```

### Configuración de Firewall

```bash
# Permitir solo acceso local (ejemplo)
sudo ufw allow from 192.168.1.0/24 to any port 443
```

### Variables de Entorno Importantes

```env
DEBUG=False
SECRET_KEY=clave-secreta-larga-y-aleatoria
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Mantenimiento

### Backup de Base de Datos

```bash
# Backup
pg_dump -U sigap_user sigap_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U sigap_user sigap_db < backup_20240101.sql
```

### Backup de Archivos

```bash
# Backup de media y static
tar -czvf sigap_backup_$(date +%Y%m%d).tar.gz media/ staticfiles/
```

### Actualización

```bash
# Detener servicio
sudo systemctl stop sigap

# Actualizar código y dependencias
git pull
pip install -r requirements.txt

# Migraciones y estáticos
python manage.py migrate
python manage.py collectstatic --noinput

# Reiniciar
sudo systemctl start sigap
```

## Soporte

Para reportar problemas o solicitar soporte:

1. Revisar logs en `logs/`
2. Contactar al administrador del sistema
3. Documentar el error con capturas de pantalla

## Roadmap

- [ ] App móvil para escaneo de códigos QR
- [ ] Integración con sistemas ERP
- [ ] Dashboard con gráficos avanzados
- [ ] Notificaciones por correo electrónico
- [ ] API REST para integraciones

## Licencia

Este software es propiedad de la empresa. Uso exclusivo para la gestión interna de activos de planta.

---

Desarrollado con Django 5 y Tailwind CSS.
