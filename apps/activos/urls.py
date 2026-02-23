"""
URLs para la app activos del proyecto SIGAP.
"""
from django.urls import path
from . import views

app_name = 'activos'

urlpatterns = [
    # TipoActivo URLs
    path('tipos/', views.TipoActivoListView.as_view(), name='tipoactivo_list'),
    path('tipos/<int:pk>/', views.TipoActivoDetailView.as_view(), name='tipoactivo_detail'),
    path('tipos/crear/', views.TipoActivoCreateView.as_view(), name='tipoactivo_create'),
    path('tipos/<int:pk>/editar/', views.TipoActivoUpdateView.as_view(), name='tipoactivo_update'),
    path('tipos/<int:pk>/eliminar/', views.TipoActivoDeleteView.as_view(), name='tipoactivo_delete'),
    
    # Estado URLs
    path('estados/', views.EstadoListView.as_view(), name='estado_list'),
    path('estados/<int:pk>/', views.EstadoDetailView.as_view(), name='estado_detail'),
    path('estados/crear/', views.EstadoCreateView.as_view(), name='estado_create'),
    path('estados/<int:pk>/editar/', views.EstadoUpdateView.as_view(), name='estado_update'),
    path('estados/<int:pk>/eliminar/', views.EstadoDeleteView.as_view(), name='estado_delete'),
    
    # TipoPropiedad URLs
    path('propiedades/', views.TipoPropiedadListView.as_view(), name='tipopropiedad_list'),
    path('propiedades/<int:pk>/', views.TipoPropiedadDetailView.as_view(), name='tipopropiedad_detail'),
    path('propiedades/crear/', views.TipoPropiedadCreateView.as_view(), name='tipopropiedad_create'),
    path('propiedades/<int:pk>/editar/', views.TipoPropiedadUpdateView.as_view(), name='tipopropiedad_update'),
    path('propiedades/<int:pk>/eliminar/', views.TipoPropiedadDeleteView.as_view(), name='tipopropiedad_delete'),
    
    # Activo URLs
    path('', views.ActivoListView.as_view(), name='activo_list'),
    path('<int:pk>/', views.ActivoDetailView.as_view(), name='activo_detail'),
    path('crear/', views.ActivoCreateView.as_view(), name='activo_create'),
    path('<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='activo_update'),
    path('<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='activo_delete'),
    path('<int:pk>/cambiar-estado/', views.ActivoCambiarEstadoView.as_view(), name='activo_cambiar_estado'),
    
    # EquipoFuncional URLs
    path('equipos/', views.EquipoFuncionalListView.as_view(), name='equipofuncional_list'),
    path('equipos/<int:pk>/', views.EquipoFuncionalDetailView.as_view(), name='equipofuncional_detail'),
    path('equipos/crear/', views.EquipoFuncionalCreateView.as_view(), name='equipofuncional_create'),
    path('equipos/<int:pk>/editar/', views.EquipoFuncionalUpdateView.as_view(), name='equipofuncional_update'),
    path('equipos/<int:pk>/eliminar/', views.EquipoFuncionalDeleteView.as_view(), name='equipofuncional_delete'),
    
    # API AJAX
    path('ajax/niveles/', views.get_niveles_by_planta, name='ajax_niveles'),
    path('ajax/areas/', views.get_areas_by_nivel, name='ajax_areas'),
    path('ajax/subareas/', views.get_subareas_by_area, name='ajax_subareas'),
]
