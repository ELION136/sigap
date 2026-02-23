#!/bin/bash
# Script de inicio rápido para SIGAP
# Uso: ./scripts/quickstart.sh

set -e

echo "=========================================="
echo "SIGAP - Inicio Rápido"
echo "=========================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION detectado${NC}"

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}Advertencia: PostgreSQL no está instalado${NC}"
    echo "Instale PostgreSQL antes de continuar"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL detectado${NC}"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo ""
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
fi

# Activar entorno virtual
echo ""
echo "Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"

# Instalar dependencias
echo ""
echo "Instalando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo ""
    echo "Creando archivo de configuración..."
    cp .env.example .env
    echo -e "${YELLOW}! Archivo .env creado. Por favor, edítelo con sus configuraciones${NC}"
fi

# Crear directorios necesarios
echo ""
echo "Creando directorios..."
mkdir -p media staticfiles logs
echo -e "${GREEN}✓ Directorios creados${NC}"

# Verificar conexión a base de datos
echo ""
echo "Verificando conexión a base de datos..."
if python3 -c "
import os
import environ
env = environ.Env()
env.read_env('.env')
import psycopg2
try:
    conn = psycopg2.connect(
        dbname=env('DB_NAME'),
        user=env('DB_USER'),
        password=env('DB_PASSWORD'),
        host=env('DB_HOST'),
        port=env('DB_PORT')
    )
    conn.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
    echo -e "${GREEN}✓ Conexión a base de datos exitosa${NC}"
else
    echo -e "${RED}✗ No se pudo conectar a la base de datos${NC}"
    echo "Verifique que PostgreSQL esté corriendo y la configuración en .env sea correcta"
    exit 1
fi

# Ejecutar migraciones
echo ""
echo "Ejecutando migraciones..."
python manage.py migrate --run-syncdb
echo -e "${GREEN}✓ Migraciones completadas${NC}"

# Cargar datos iniciales
echo ""
echo "Cargando datos iniciales..."
python manage.py loaddata fixtures/initial_data.json 2>/dev/null || echo -e "${YELLOW}! Datos iniciales ya cargados${NC}"
echo -e "${GREEN}✓ Datos iniciales cargados${NC}"

# Configurar grupos
echo ""
echo "Configurando grupos y permisos..."
python manage.py shell < scripts/setup_groups.py
echo -e "${GREEN}✓ Grupos configurados${NC}"

# Verificar superusuario
echo ""
echo "Verificando superusuario..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" 2>/dev/null; then
    echo -e "${GREEN}✓ Superusuario existe${NC}"
else
    echo -e "${YELLOW}! No hay superusuario configurado${NC}"
    echo "Ejecute: python manage.py createsuperuser"
fi

# Recolectar estáticos
echo ""
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput -v 0
echo -e "${GREEN}✓ Archivos estáticos recolectados${NC}"

# Verificación final
echo ""
echo "Verificando instalación..."
python manage.py check
echo -e "${GREEN}✓ Verificación completada${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}¡SIGAP está listo para usar!${NC}"
echo "=========================================="
echo ""
echo "Para iniciar el servidor de desarrollo:"
echo "  python manage.py runserver"
echo ""
echo "Para iniciar con Gunicorn (producción):"
echo "  gunicorn config.wsgi:application -c gunicorn.conf.py"
echo ""
echo "Acceda al sistema en:"
echo "  http://localhost:8000"
echo ""
echo "Panel de administración:"
echo "  http://localhost:8000/admin/"
echo ""
