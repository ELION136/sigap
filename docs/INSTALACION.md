# Guía de Instalación - SIGAP

Sistema Integral de Gestión de Activos de Planta

## Requisitos del Sistema

### Software Necesario

- **Python** >= 3.10
- **PostgreSQL** >= 13
- **Node.js** >= 18 (opcional, para desarrollo frontend)
- **Git**

### Hardware Recomendado

- **RAM**: Mínimo 4 GB (8 GB recomendado)
- **Disco**: 20 GB de espacio libre
- **Procesador**: 2 núcleos o más

---

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd sigap
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Activar en Linux/Mac
source venv/bin/activate

# Activar en Windows
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Base de Datos PostgreSQL

```bash
# Conectarse a PostgreSQL
sudo -u postgres psql

# Crear usuario y base de datos
CREATE USER sigap_user WITH PASSWORD 'sigap_secure_password_2024';
CREATE DATABASE sigap_db OWNER sigap_user;
GRANT ALL PRIVILEGES ON DATABASE sigap_db TO sigap_user;
\q
```

### 5. Configurar Variables de Entorno

```bash
cp .env.example .env
```

Editar el archivo `.env` con los valores apropiados:

```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100

DB_NAME=sigap_db
DB_USER=sigap_user
DB_PASSWORD=sigap_secure_password_2024
DB_HOST=localhost
DB_PORT=5432
```

### 6. Crear Directorios Necesarios

```bash
mkdir -p media staticfiles logs
```

### 7. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 8. Cargar Datos Iniciales

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 9. Configurar Grupos y Permisos

```bash
python manage.py shell < scripts/setup_groups.py
```

### 10. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 11. Recolectar Archivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 12. Verificar Instalación

```bash
python manage.py check
```

---

## Configuración para Producción (Intranet)

### 1. Configurar Firewall

```bash
# Ubuntu/Debian con UFW
sudo ufw allow 8000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Configurar Gunicorn

Crear archivo `gunicorn.conf.py`:

```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5
errorlog = "logs/gunicorn-error.log"
accesslog = "logs/gunicorn-access.log"
capture_output = True
enable_stdio_inheritance = True
```

### 3. Generar Certificado SSL Autofirmado

```bash
# Crear directorio para certificados
mkdir -p certs

# Generar certificado
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout certs/sigap.key \
    -out certs/sigap.crt \
    -subj "/C=MX/ST=Estado/L=Ciudad/O=Mi Empresa/OU=IT/CN=sigap.intranet"

# Establecer permisos seguros
chmod 600 certs/sigap.key
chmod 644 certs/sigap.crt
```

### 4. Configurar Nginx (Opcional pero recomendado)

```nginx
server {
    listen 80;
    server_name sigap.intranet 192.168.1.100;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name sigap.intranet 192.168.1.100;

    ssl_certificate /ruta/a/certs/sigap.crt;
    ssl_certificate_key /ruta/a/certs/sigap.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 20M;

    location /static/ {
        alias /ruta/a/sigap/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /ruta/a/sigap/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Iniciar el Servidor

```bash
# Con Gunicorn
gunicorn config.wsgi:application -c gunicorn.conf.py

# O con el servidor de desarrollo (solo para pruebas)
python manage.py runserver 0.0.0.0:8000
```

---

## Configuración de Servicio Systemd

Crear archivo `/etc/systemd/system/sigap.service`:

```ini
[Unit]
Description=SIGAP - Sistema de Gestión de Activos
After=network.target

[Service]
User=sigap
Group=sigap
WorkingDirectory=/ruta/a/sigap
Environment="PATH=/ruta/a/sigap/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=config.settings"
ExecStart=/ruta/a/sigap/venv/bin/gunicorn config.wsgi:application -c gunicorn.conf.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Habilitar y iniciar el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sigap
sudo systemctl start sigap
sudo systemctl status sigap
```

---

## Actualización del Sistema

```bash
# 1. Detener el servicio
sudo systemctl stop sigap

# 2. Actualizar código
git pull

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Actualizar dependencias
pip install -r requirements.txt

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Recolectar estáticos
python manage.py collectstatic --noinput

# 7. Reiniciar servicio
sudo systemctl start sigap
```

---

## Solución de Problemas

### Error de conexión a PostgreSQL

```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Verificar configuración de pg_hba.conf
sudo nano /etc/postgresql/13/main/pg_hba.conf
# Asegurarse de tener: local all all md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### Permisos de archivos estáticos

```bash
# Establecer permisos correctos
sudo chown -R www-data:www-data /ruta/a/sigap/staticfiles
sudo chown -R www-data:www-data /ruta/a/sigap/media
```

### Errores de SSL

```bash
# Verificar certificado
openssl x509 -in certs/sigap.crt -text -noout

# Verificar que la clave coincida
openssl rsa -in certs/sigap.key -check
```

---

## Contacto y Soporte

Para soporte técnico, contactar al administrador del sistema.

---

## Licencia

Este software es propiedad de la empresa. Uso exclusivo para la gestión interna de activos.
