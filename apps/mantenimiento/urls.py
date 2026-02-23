"""
URLs para la app mantenimiento del proyecto SIGAP.
"""
from django.urls import path
from . import views

app_name = 'mantenimiento'

urlpatterns = [
    # TipoMantenimiento URLs
    path('tipos/', views.TipoMantenimientoListView.as_view(), name='tipomantenimiento_list'),
    path('tipos/<int:pk>/', views.TipoMantenimientoDetailView.as_view(), name='tipomantenimiento_detail'),
    path('tipos/crear/', views.TipoMantenimientoCreateView.as_view(), name='tipomantenimiento_create'),
    path('tipos/<int:pk>/editar/', views.TipoMantenimientoUpdateView.as_view(), name='tipomantenimiento_update'),
    path('tipos/<int:pk>/eliminar/', views.TipoMantenimientoDeleteView.as_view(), name='tipomantenimiento_delete'),
    
    # Mantenimiento URLs
    path('', views.MantenimientoListView.as_view(), name='mantenimiento_list'),
    path('<int:pk>/', views.MantenimientoDetailView.as_view(), name='mantenimiento_detail'),
    path('crear/', views.MantenimientoCreateView.as_view(), name='mantenimiento_create'),
    path('crear-rapido/', views.MantenimientoQuickCreateView.as_view(), name='mantenimiento_quick_create'),
    path('<int:pk>/editar/', views.MantenimientoUpdateView.as_view(), name='mantenimiento_update'),
    path('<int:pk>/eliminar/', views.MantenimientoDeleteView.as_view(), name='mantenimiento_delete'),
    
    # RepuestoUtilizado URLs
    path('<int:mantenimiento_pk>/repuestos/agregar/', 
         views.RepuestoUtilizadoCreateView.as_view(), name='repuesto_create'),
    path('repuestos/<int:pk>/editar/', 
         views.RepuestoUtilizadoUpdateView.as_view(), name='repuesto_update'),
    path('repuestos/<int:pk>/eliminar/', 
         views.RepuestoUtilizadoDeleteView.as_view(), name='repuesto_delete'),
]
