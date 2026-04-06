"""
URLs para la app reportes del proyecto SIGAP.
"""
from django.urls import path
from . import views
from .views import exportar_mantenimientos_pdf
from .views import exportar_activos_pdf
from .views import exportar_equipos_pdf

app_name = 'reportes'

urlpatterns = [
    path('', views.ReporteIndexView.as_view(), name='index'),
    
    # Reportes HTML
    path('activos/', views.reporte_activos, name='reporte_activos'),
    path('mantenimientos/', views.reporte_mantenimientos, name='reporte_mantenimientos'),
    path('equipos/', views.reporte_equipos, name='reporte_equipos'),
    
    # Exportaciones Excel
    path('exportar/activos/', views.exportar_activos_excel, name='exportar_activos'),
    path('exportar/mantenimientos/', views.exportar_mantenimientos_excel, name='exportar_mantenimientos'),
    
    # API
    path('api/dashboard/', views.dashboard_data, name='dashboard_data'),

    path('mantenimientos/pdf/', exportar_mantenimientos_pdf, name='exportar_mantenimientos_pdf'),
    path('exportar/activos/pdf/', exportar_activos_pdf, name='exportar_activos_pdf'),
    path('exportar/equipos/pdf/', exportar_equipos_pdf, name='exportar_equipos_pdf'),
]
