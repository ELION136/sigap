"""
URLs para la app organizacion del proyecto SIGAP.
"""
from django.urls import path
from . import views

app_name = 'organizacion'

urlpatterns = [
    # Planta URLs
    path('plantas/', views.PlantaListView.as_view(), name='planta_list'),
    path('plantas/<int:pk>/', views.PlantaDetailView.as_view(), name='planta_detail'),
    path('plantas/crear/', views.PlantaCreateView.as_view(), name='planta_create'),
    path('plantas/<int:pk>/editar/', views.PlantaUpdateView.as_view(), name='planta_update'),
    path('plantas/<int:pk>/eliminar/', views.PlantaDeleteView.as_view(), name='planta_delete'),
    
    # Nivel URLs
    path('niveles/', views.NivelListView.as_view(), name='nivel_list'),
    path('niveles/<int:pk>/', views.NivelDetailView.as_view(), name='nivel_detail'),
    path('niveles/crear/', views.NivelCreateView.as_view(), name='nivel_create'),
    path('niveles/<int:pk>/editar/', views.NivelUpdateView.as_view(), name='nivel_update'),
    path('niveles/<int:pk>/eliminar/', views.NivelDeleteView.as_view(), name='nivel_delete'),
    
    # Area URLs
    path('areas/', views.AreaListView.as_view(), name='area_list'),
    path('areas/<int:pk>/', views.AreaDetailView.as_view(), name='area_detail'),
    path('areas/crear/', views.AreaCreateView.as_view(), name='area_create'),
    path('areas/<int:pk>/editar/', views.AreaUpdateView.as_view(), name='area_update'),
    path('areas/<int:pk>/eliminar/', views.AreaDeleteView.as_view(), name='area_delete'),
    
    # SubArea URLs
    path('subareas/', views.SubAreaListView.as_view(), name='subarea_list'),
    path('subareas/<int:pk>/', views.SubAreaDetailView.as_view(), name='subarea_detail'),
    path('subareas/crear/', views.SubAreaCreateView.as_view(), name='subarea_create'),
    path('subareas/<int:pk>/editar/', views.SubAreaUpdateView.as_view(), name='subarea_update'),
    path('subareas/<int:pk>/eliminar/', views.SubAreaDeleteView.as_view(), name='subarea_delete'),
    
    # Responsable URLs
    path('responsables/', views.ResponsableListView.as_view(), name='responsable_list'),
    path('responsables/<int:pk>/', views.ResponsableDetailView.as_view(), name='responsable_detail'),
    path('responsables/crear/', views.ResponsableCreateView.as_view(), name='responsable_create'),
    path('responsables/<int:pk>/editar/', views.ResponsableUpdateView.as_view(), name='responsable_update'),
    path('responsables/<int:pk>/eliminar/', views.ResponsableDeleteView.as_view(), name='responsable_delete'),
]
