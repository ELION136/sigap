"""
Tests para la app core del proyecto SIGAP.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import HistorialCambio, ConfiguracionSistema


User = get_user_model()


class HistorialCambioModelTest(TestCase):
    """Tests para el modelo HistorialCambio."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_crear_historial(self):
        """Test creación de registro de historial."""
        historial = HistorialCambio.registrar(
            tipo_operacion='CREAR',
            modelo='Activo',
            objeto_id=1,
            objeto_repr='Activo de prueba',
            usuario=self.user,
            descripcion='Prueba de creación'
        )
        
        self.assertEqual(historial.tipo_operacion, 'CREAR')
        self.assertEqual(historial.modelo, 'Activo')
        self.assertEqual(historial.usuario, self.user)
    
    def test_str_representation(self):
        """Test representación en string."""
        historial = HistorialCambio.registrar(
            tipo_operacion='MODIFICAR',
            modelo='Activo',
            objeto_id=1,
            objeto_repr='Activo de prueba'
        )
        
        self.assertIn('Modificación', str(historial))
        self.assertIn('Activo', str(historial))


class ConfiguracionSistemaModelTest(TestCase):
    """Tests para el modelo ConfiguracionSistema."""
    
    def test_crear_configuracion(self):
        """Test creación de configuración."""
        config = ConfiguracionSistema.objects.create(
            clave='TEST_CONFIG',
            valor='test_value',
            descripcion='Configuración de prueba',
            tipo='string'
        )
        
        self.assertEqual(config.clave, 'TEST_CONFIG')
        self.assertEqual(config.get_valor(), 'test_value')
    
    def test_get_valor_int(self):
        """Test obtener valor entero."""
        config = ConfiguracionSistema.objects.create(
            clave='TEST_INT',
            valor='42',
            tipo='int'
        )
        
        self.assertEqual(config.get_valor(), 42)
    
    def test_get_valor_bool(self):
        """Test obtener valor booleano."""
        config = ConfiguracionSistema.objects.create(
            clave='TEST_BOOL',
            valor='true',
            tipo='bool'
        )
        
        self.assertTrue(config.get_valor())


class DashboardViewTest(TestCase):
    """Tests para la vista del dashboard."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_dashboard_login_required(self):
        """Test que el dashboard requiere login."""
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_dashboard_accessible(self):
        """Test que el dashboard es accesible para usuarios logueados."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/dashboard.html')


class SecurityHeadersTest(TestCase):
    """Tests para headers de seguridad."""
    
    def setUp(self):
        self.client = Client()
    
    def test_security_headers(self):
        """Test que los headers de seguridad están presentes."""
        response = self.client.get('/accounts/login/')
        
        # Verificar headers de seguridad
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.get('X-XSS-Protection'), '1; mode=block')
