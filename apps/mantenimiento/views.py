"""
Vistas para la app mantenimiento del proyecto SIGAP.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone

from .models import TipoMantenimiento, Mantenimiento, RepuestoUtilizado
from .forms import (
    TipoMantenimientoForm, MantenimientoForm, 
    MantenimientoQuickForm, RepuestoUtilizadoForm
)


class BaseListView(LoginRequiredMixin, ListView):
    """Vista base para listados con búsqueda."""
    paginate_by = 25
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class BaseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista base para crear registros."""
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user
        messages.success(
            self.request, 
            f'{self.model._meta.verbose_name} creado exitosamente.'
        )
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista base para actualizar registros."""
    
    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name} actualizado exitosamente.'
        )
        return super().form_valid(form)


class BaseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista base para eliminar registros."""
    
    def delete(self, request, *args, **kwargs):
        messages.success(
            request,
            f'{self.model._meta.verbose_name} eliminado exitosamente.'
        )
        return super().delete(request, *args, **kwargs)


# =============================================================================
# VISTAS PARA TIPOMANTENIMIENTO
# =============================================================================

class TipoMantenimientoListView(BaseListView):
    """Vista de lista para Tipos de Mantenimiento."""
    model = TipoMantenimiento
    template_name = 'mantenimiento/tipomantenimiento_list.html'
    context_object_name = 'tipos'
    permission_required = 'mantenimiento.view_tipomantenimiento'


class TipoMantenimientoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Tipo de Mantenimiento."""
    model = TipoMantenimiento
    template_name = 'mantenimiento/tipomantenimiento_detail.html'
    context_object_name = 'tipo'
    permission_required = 'mantenimiento.view_tipomantenimiento'


class TipoMantenimientoCreateView(BaseCreateView):
    """Vista para crear Tipo de Mantenimiento."""
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'mantenimiento/tipomantenimiento_form.html'
    permission_required = 'mantenimiento.add_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')


class TipoMantenimientoUpdateView(BaseUpdateView):
    """Vista para actualizar Tipo de Mantenimiento."""
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'mantenimiento/tipomantenimiento_form.html'
    permission_required = 'mantenimiento.change_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')


class TipoMantenimientoDeleteView(BaseDeleteView):
    """Vista para eliminar Tipo de Mantenimiento."""
    model = TipoMantenimiento
    template_name = 'mantenimiento/tipomantenimiento_confirm_delete.html'
    permission_required = 'mantenimiento.delete_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')


# =============================================================================
# VISTAS PARA MANTENIMIENTO
# =============================================================================

class MantenimientoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista de lista para Mantenimientos."""
    model = Mantenimiento
    template_name = 'mantenimiento/mantenimiento_list.html'
    context_object_name = 'mantenimientos'
    permission_required = 'mantenimiento.view_mantenimiento'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Mantenimiento.objects.select_related(
            'activo', 'solicitado_por', 'realizado_por'
        )
        
        # Filtros
        search = self.request.GET.get('q')
        tipo = self.request.GET.get('tipo')
        estado = self.request.GET.get('estado')
        prioridad = self.request.GET.get('prioridad')
        activo = self.request.GET.get('activo')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(activo__nombre__icontains=search) |
                Q(activo__codigo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if activo:
            queryset = queryset.filter(activo_id=activo)
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        
        return queryset.order_by('-fecha')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Mantenimiento.TIPO_MANTENIMIENTO
        context['estados'] = Mantenimiento.ESTADO_MANTENIMIENTO
        context['prioridades'] = Mantenimiento.PRIORIDAD
        context['activos'] = Activo.objects.filter(activo_registro=True)
        
        # Estadísticas
        hoy = timezone.now().date()
        context['stats'] = {
            'pendientes': Mantenimiento.objects.filter(estado='PENDIENTE').count(),
            'en_progreso': Mantenimiento.objects.filter(estado='EN_PROGRESO').count(),
            'completados_mes': Mantenimiento.objects.filter(
                estado='COMPLETADO',
                fecha_realizacion__month=hoy.month,
                fecha_realizacion__year=hoy.year
            ).count(),
            'vencidos': Mantenimiento.objects.filter(
                estado='PENDIENTE',
                fecha__lt=hoy
            ).count(),
        }
        
        # Preservar filtros
        context['filtros'] = {
            'q': self.request.GET.get('q', ''),
            'tipo': self.request.GET.get('tipo', ''),
            'estado': self.request.GET.get('estado', ''),
            'prioridad': self.request.GET.get('prioridad', ''),
            'activo': self.request.GET.get('activo', ''),
            'fecha_desde': self.request.GET.get('fecha_desde', ''),
            'fecha_hasta': self.request.GET.get('fecha_hasta', ''),
        }
        return context


class MantenimientoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Mantenimiento."""
    model = Mantenimiento
    template_name = 'mantenimiento/mantenimiento_detail.html'
    context_object_name = 'mantenimiento'
    permission_required = 'mantenimiento.view_mantenimiento'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'activo', 'solicitado_por', 'realizado_por'
        ).prefetch_related('repuestos')


class MantenimientoCreateView(BaseCreateView):
    """Vista para crear Mantenimiento."""
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'mantenimiento/mantenimiento_form.html'
    permission_required = 'mantenimiento.add_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')


class MantenimientoUpdateView(BaseUpdateView):
    """Vista para actualizar Mantenimiento."""
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'mantenimiento/mantenimiento_form.html'
    permission_required = 'mantenimiento.change_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')


class MantenimientoDeleteView(BaseDeleteView):
    """Vista para eliminar Mantenimiento."""
    model = Mantenimiento
    template_name = 'mantenimiento/mantenimiento_confirm_delete.html'
    permission_required = 'mantenimiento.delete_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')


class MantenimientoQuickCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para crear mantenimiento rápido."""
    model = Mantenimiento
    form_class = MantenimientoQuickForm
    template_name = 'mantenimiento/mantenimiento_quick_form.html'
    permission_required = 'mantenimiento.add_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user
        messages.success(
            self.request, 
            'Mantenimiento creado exitosamente.'
        )
        return super().form_valid(form)


# =============================================================================
# VISTAS PARA REPUESTOS
# =============================================================================

class RepuestoUtilizadoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Vista para agregar repuesto a un mantenimiento."""
    model = RepuestoUtilizado
    form_class = RepuestoUtilizadoForm
    template_name = 'mantenimiento/repuesto_form.html'
    permission_required = 'mantenimiento.add_repuestoutilizado'
    
    def dispatch(self, request, *args, **kwargs):
        self.mantenimiento = get_object_or_404(Mantenimiento, pk=kwargs['mantenimiento_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.mantenimiento = self.mantenimiento
        form.instance.creado_por = self.request.user
        form.instance.modificado_por = self.request.user
        messages.success(self.request, 'Repuesto agregado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantenimiento_detail', kwargs={'pk': self.mantenimiento.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mantenimiento'] = self.mantenimiento
        return context


class RepuestoUtilizadoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista para actualizar repuesto."""
    model = RepuestoUtilizado
    form_class = RepuestoUtilizadoForm
    template_name = 'mantenimiento/repuesto_form.html'
    permission_required = 'mantenimiento.change_repuestoutilizado'
    
    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        messages.success(self.request, 'Repuesto actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantenimiento_detail', kwargs={'pk': self.object.mantenimiento.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mantenimiento'] = self.object.mantenimiento
        return context


class RepuestoUtilizadoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Vista para eliminar repuesto."""
    model = RepuestoUtilizado
    template_name = 'mantenimiento/repuesto_confirm_delete.html'
    permission_required = 'mantenimiento.delete_repuestoutilizado'
    
    def delete(self, request, *args, **kwargs):
        self.mantenimiento_pk = self.get_object().mantenimiento.pk
        messages.success(request, 'Repuesto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('mantenimiento:mantenimiento_detail', kwargs={'pk': self.mantenimiento_pk})
