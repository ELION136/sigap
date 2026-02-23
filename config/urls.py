"""
Configuración de URLs para el proyecto SIGAP.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
    
    # Aplicaciones
    path('', include('apps.core.urls')),
    path('organizacion/', include('apps.organizacion.urls')),
    path('activos/', include('apps.activos.urls')),
    path('mantenimiento/', include('apps.mantenimiento.urls')),
    path('reportes/', include('apps.reportes.urls')),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
