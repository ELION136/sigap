"""
Vistas para la app core del proyecto SIGAP.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.activos.models import Activo, EquipoFuncional
from apps.mantenimiento.models import Mantenimiento
from apps.organizacion.models import Planta, Area
from .models import HistorialCambio


class SuperUserRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere que el usuario sea superusuario."""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(
            name='Administrador'
        ).exists()


@login_required
def dashboard(request):
    """
    Vista del dashboard principal con resúmenes y estadísticas.
    """
    context = {}
    
    # Estadísticas generales
    context['total_activos'] = Activo.objects.count()
    context['total_equipos'] = EquipoFuncional.objects.count()
    context['total_plantas'] = Planta.objects.count()
    context['total_areas'] = Area.objects.count()
    
    # Activos por estado
    context['activos_por_estado'] = Activo.objects.values(
        'estado__nombre', 'estado__color'
    ).annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')
    
    # Activos por tipo
    context['activos_por_tipo'] = Activo.objects.values(
        'tipo__nombre'
    ).annotate(
        cantidad=Count('id')
    ).order_by('-cantidad')[:5]
    
    # Mantenimientos recientes
    context['mantenimientos_recientes'] = Mantenimiento.objects.select_related(
        'activo'
    ).order_by('-fecha')[:5]
    
    # Mantenimientos próximos (próximos 30 días)
    hoy = timezone.now().date()
    proximos_30_dias = hoy + timedelta(days=30)
    context['mantenimientos_proximos'] = Mantenimiento.objects.filter(
        fecha__gte=hoy,
        fecha__lte=proximos_30_dias,
        estado='PENDIENTE'
    ).select_related('activo').order_by('fecha')[:5]
    
    # Activos sin mantenimiento en los últimos 6 meses
    hace_6_meses = hoy - timedelta(days=180)
    context['activos_sin_mantenimiento'] = Activo.objects.filter(
        Q(mantenimientos__fecha__lt=hace_6_meses) | 
        Q(mantenimientos__isnull=True)
    ).distinct()[:5]
    
    # Últimos cambios en el sistema
    context['ultimos_cambios'] = HistorialCambio.objects.select_related(
        'usuario'
    ).order_by('-fecha_hora')[:10]
    
    # Alertas
    context['alertas'] = []
    
    # Alerta: Activos fuera de servicio
    activos_fuera_servicio = Activo.objects.filter(
        estado__nombre__icontains='fuera'
    ).count()
    if activos_fuera_servicio > 0:
        context['alertas'].append({
            'tipo': 'warning',
            'mensaje': f'{activos_fuera_servicio} activos fuera de servicio',
            'icono': 'exclamation-triangle'
        })
    
    # Alerta: Mantenimientos vencidos
    mantenimientos_vencidos = Mantenimiento.objects.filter(
        fecha__lt=hoy,
        estado='PENDIENTE'
    ).count()
    if mantenimientos_vencidos > 0:
        context['alertas'].append({
            'tipo': 'danger',
            'mensaje': f'{mantenimientos_vencidos} mantenimientos vencidos',
            'icono': 'exclamation-circle'
        })
    
    return render(request, 'core/dashboard.html', context)


class AuditoriaListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    """
    Vista de lista para el historial de auditoría.
    """
    model = HistorialCambio
    template_name = 'core/auditoria_list.html'
    context_object_name = 'cambios'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('usuario')
        
        # Filtros
        tipo = self.request.GET.get('tipo')
        modelo = self.request.GET.get('modelo')
        usuario = self.request.GET.get('usuario')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if tipo:
            queryset = queryset.filter(tipo_operacion=tipo)
        if modelo:
            queryset = queryset.filter(modelo__icontains=modelo)
        if usuario:
            queryset = queryset.filter(usuario__username__icontains=usuario)
        if fecha_desde:
            queryset = queryset.filter(fecha_hora__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_hora__date__lte=fecha_hasta)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_operacion'] = HistorialCambio.TIPO_OPERACION
        context['modelos'] = HistorialCambio.objects.values_list(
            'modelo', flat=True
        ).distinct()
        
        # Preservar filtros en la paginación
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()
        
        return context
