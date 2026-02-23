"""
Configuración de Gunicorn para SIGAP
"""
import os
import multiprocessing

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = 'logs/gunicorn-access.log'
errorlog = 'logs/gunicorn-error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'sigap'

# Server mechanics
daemon = False
pidfile = 'logs/gunicorn.pid'

# SSL (configurar en producción)
# keyfile = 'certs/sigap.key'
# certfile = 'certs/sigap.crt'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server hooks
def on_starting(server):
    """Llamado justo antes de que el proceso maestro se inicialice."""
    pass

def on_reload(server):
    """Llamado cuando recibe la señal SIGHUP."""
    pass

def when_ready(server):
    """Llamado justo después de que el servidor se inicia."""
    pass

def worker_int(worker):
    """Llamado cuando un worker recibe SIGINT o SIGQUIT."""
    pass

def worker_abort(worker):
    """Llamado cuando un worker recibe SIGABRT."""
    pass
