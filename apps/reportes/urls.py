"""
URLs para la app reportes del proyecto SIGAP.
"""
from django.urls import path
from . import views

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
]
