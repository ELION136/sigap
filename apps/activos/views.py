"""
Vistas para la app activos del proyecto SIGAP.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse

from .models import TipoActivo, Estado, TipoPropiedad, Activo, EquipoFuncional
from .forms import (
    TipoActivoForm, EstadoForm, TipoPropiedadForm,
    ActivoForm, ActivoEstadoForm, EquipoFuncionalForm
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
# VISTAS PARA TIPOACTIVO
# =============================================================================

class TipoActivoListView(BaseListView):
    """Vista de lista para Tipos de Activo."""
    model = TipoActivo
    template_name = 'activos/tipoactivo_list.html'
    context_object_name = 'tipos'
    permission_required = 'activos.view_tipoactivo'


class TipoActivoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Tipo de Activo."""
    model = TipoActivo
    template_name = 'activos/tipoactivo_detail.html'
    context_object_name = 'tipo'
    permission_required = 'activos.view_tipoactivo'


class TipoActivoCreateView(BaseCreateView):
    """Vista para crear Tipo de Activo."""
    model = TipoActivo
    form_class = TipoActivoForm
    template_name = 'activos/tipoactivo_form.html'
    permission_required = 'activos.add_tipoactivo'
    success_url = reverse_lazy('activos:tipoactivo_list')


class TipoActivoUpdateView(BaseUpdateView):
    """Vista para actualizar Tipo de Activo."""
    model = TipoActivo
    form_class = TipoActivoForm
    template_name = 'activos/tipoactivo_form.html'
    permission_required = 'activos.change_tipoactivo'
    success_url = reverse_lazy('activos:tipoactivo_list')


class TipoActivoDeleteView(BaseDeleteView):
    """Vista para eliminar Tipo de Activo."""
    model = TipoActivo
    template_name = 'activos/tipoactivo_confirm_delete.html'
    permission_required = 'activos.delete_tipoactivo'
    success_url = reverse_lazy('activos:tipoactivo_list')


# =============================================================================
# VISTAS PARA ESTADO
# =============================================================================

class EstadoListView(BaseListView):
    """Vista de lista para Estados."""
    model = Estado
    template_name = 'activos/estado_list.html'
    context_object_name = 'estados'
    permission_required = 'activos.view_estado'


class EstadoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Estado."""
    model = Estado
    template_name = 'activos/estado_detail.html'
    context_object_name = 'estado'
    permission_required = 'activos.view_estado'


class EstadoCreateView(BaseCreateView):
    """Vista para crear Estado."""
    model = Estado
    form_class = EstadoForm
    template_name = 'activos/estado_form.html'
    permission_required = 'activos.add_estado'
    success_url = reverse_lazy('activos:estado_list')


class EstadoUpdateView(BaseUpdateView):
    """Vista para actualizar Estado."""
    model = Estado
    form_class = EstadoForm
    template_name = 'activos/estado_form.html'
    permission_required = 'activos.change_estado'
    success_url = reverse_lazy('activos:estado_list')


class EstadoDeleteView(BaseDeleteView):
    """Vista para eliminar Estado."""
    model = Estado
    template_name = 'activos/estado_confirm_delete.html'
    permission_required = 'activos.delete_estado'
    success_url = reverse_lazy('activos:estado_list')


# =============================================================================
# VISTAS PARA TIPOPROPIEDAD
# =============================================================================

class TipoPropiedadListView(BaseListView):
    """Vista de lista para Tipos de Propiedad."""
    model = TipoPropiedad
    template_name = 'activos/tipopropiedad_list.html'
    context_object_name = 'tipos_propiedad'
    permission_required = 'activos.view_tipopropiedad'


class TipoPropiedadDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Tipo de Propiedad."""
    model = TipoPropiedad
    template_name = 'activos/tipopropiedad_detail.html'
    context_object_name = 'tipo_propiedad'
    permission_required = 'activos.view_tipopropiedad'


class TipoPropiedadCreateView(BaseCreateView):
    """Vista para crear Tipo de Propiedad."""
    model = TipoPropiedad
    form_class = TipoPropiedadForm
    template_name = 'activos/tipopropiedad_form.html'
    permission_required = 'activos.add_tipopropiedad'
    success_url = reverse_lazy('activos:tipopropiedad_list')


class TipoPropiedadUpdateView(BaseUpdateView):
    """Vista para actualizar Tipo de Propiedad."""
    model = TipoPropiedad
    form_class = TipoPropiedadForm
    template_name = 'activos/tipopropiedad_form.html'
    permission_required = 'activos.change_tipopropiedad'
    success_url = reverse_lazy('activos:tipopropiedad_list')


class TipoPropiedadDeleteView(BaseDeleteView):
    """Vista para eliminar Tipo de Propiedad."""
    model = TipoPropiedad
    template_name = 'activos/tipopropiedad_confirm_delete.html'
    permission_required = 'activos.delete_tipopropiedad'
    success_url = reverse_lazy('activos:tipopropiedad_list')


# =============================================================================
# VISTAS PARA ACTIVO
# =============================================================================

class ActivoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista de lista para Activos."""
    model = Activo
    template_name = 'activos/activo_list.html'
    context_object_name = 'activos'
    permission_required = 'activos.view_activo'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = Activo.objects.select_related(
            'tipo', 'estado', 'tipo_propiedad', 'responsable', 'ubicacion'
        )
        
        # Filtros
        search = self.request.GET.get('q')
        tipo = self.request.GET.get('tipo')
        estado = self.request.GET.get('estado')
        planta = self.request.GET.get('planta')
        responsable = self.request.GET.get('responsable')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search) |
                Q(numero_serie__icontains=search) |
                Q(marca__icontains=search)
            )
        if tipo:
            queryset = queryset.filter(tipo_id=tipo)
        if estado:
            queryset = queryset.filter(estado_id=estado)
        if planta:
            queryset = queryset.filter(ubicacion__planta_id=planta)
        if responsable:
            queryset = queryset.filter(responsable_id=responsable)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = TipoActivo.objects.filter(activo=True)
        context['estados'] = Estado.objects.filter(activo=True)
        context['plantas'] = Planta.objects.filter(activa=True)
        context['responsables'] = Responsable.objects.filter(activo=True)
        
        # Preservar filtros
        context['filtros'] = {
            'q': self.request.GET.get('q', ''),
            'tipo': self.request.GET.get('tipo', ''),
            'estado': self.request.GET.get('estado', ''),
            'planta': self.request.GET.get('planta', ''),
            'responsable': self.request.GET.get('responsable', ''),
        }
        return context


class ActivoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Activo."""
    model = Activo
    template_name = 'activos/activo_detail.html'
    context_object_name = 'activo'
    permission_required = 'activos.view_activo'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'tipo', 'estado', 'tipo_propiedad', 'responsable', 'ubicacion'
        ).prefetch_related('mantenimientos', 'equipos_funcionales')


class ActivoCreateView(BaseCreateView):
    """Vista para crear Activo."""
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/activo_form.html'
    permission_required = 'activos.add_activo'
    success_url = reverse_lazy('activos:activo_list')


class ActivoUpdateView(BaseUpdateView):
    """Vista para actualizar Activo."""
    model = Activo
    form_class = ActivoForm
    template_name = 'activos/activo_form.html'
    permission_required = 'activos.change_activo'
    success_url = reverse_lazy('activos:activo_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Prellenar campos de ubicación si existe
        if self.object and self.object.ubicacion:
            initial = kwargs.get('initial', {})
            initial['planta'] = self.object.ubicacion.planta
            initial['nivel'] = self.object.ubicacion.nivel
            initial['area'] = self.object.ubicacion.area
            initial['subarea'] = self.object.ubicacion.subarea
            initial['ubicacion_especifica'] = self.object.ubicacion.ubicacion_especifica
            kwargs['initial'] = initial
        return kwargs


class ActivoDeleteView(BaseDeleteView):
    """Vista para eliminar Activo."""
    model = Activo
    template_name = 'activos/activo_confirm_delete.html'
    permission_required = 'activos.delete_activo'
    success_url = reverse_lazy('activos:activo_list')


class ActivoCambiarEstadoView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista para cambiar solo el estado del activo."""
    model = Activo
    form_class = ActivoEstadoForm
    template_name = 'activos/activo_cambiar_estado.html'
    permission_required = 'activos.change_activo_estado'
    
    def form_valid(self, form):
        form.instance.modificado_por = self.request.user
        messages.success(
            self.request,
            f'Estado del activo "{self.object}" cambiado exitosamente.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('activos:activo_detail', kwargs={'pk': self.object.pk})


# =============================================================================
# VISTAS PARA EQUIPOFUNCIONAL
# =============================================================================

class EquipoFuncionalListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Vista de lista para Equipos Funcionales."""
    model = EquipoFuncional
    template_name = 'activos/equipofuncional_list.html'
    context_object_name = 'equipos'
    permission_required = 'activos.view_equipofuncional'
    paginate_by = 25
    
    def get_queryset(self):
        queryset = EquipoFuncional.objects.select_related(
            'area__nivel__planta', 'responsable'
        ).annotate(activos_count=Count('activos'))
        
        search = self.request.GET.get('q')
        estado = self.request.GET.get('estado')
        criticidad = self.request.GET.get('criticidad')
        
        if search:
            queryset = queryset.filter(
                Q(codigo__icontains=search) | 
                Q(nombre__icontains=search)
            )
        if estado:
            queryset = queryset.filter(estado_operativo=estado)
        if criticidad:
            queryset = queryset.filter(criticidad=criticidad)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = EquipoFuncional._meta.get_field('estado_operativo').choices
        context['criticidades'] = EquipoFuncional._meta.get_field('criticidad').choices
        return context


class EquipoFuncionalDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Equipo Funcional."""
    model = EquipoFuncional
    template_name = 'activos/equipofuncional_detail.html'
    context_object_name = 'equipo'
    permission_required = 'activos.view_equipofuncional'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'area__nivel__planta', 'responsable'
        ).prefetch_related('activos__tipo', 'activos__estado')


class EquipoFuncionalCreateView(BaseCreateView):
    """Vista para crear Equipo Funcional."""
    model = EquipoFuncional
    form_class = EquipoFuncionalForm
    template_name = 'activos/equipofuncional_form.html'
    permission_required = 'activos.add_equipofuncional'
    success_url = reverse_lazy('activos:equipofuncional_list')


class EquipoFuncionalUpdateView(BaseUpdateView):
    """Vista para actualizar Equipo Funcional."""
    model = EquipoFuncional
    form_class = EquipoFuncionalForm
    template_name = 'activos/equipofuncional_form.html'
    permission_required = 'activos.change_equipofuncional'
    success_url = reverse_lazy('activos:equipofuncional_list')


class EquipoFuncionalDeleteView(BaseDeleteView):
    """Vista para eliminar Equipo Funcional."""
    model = EquipoFuncional
    template_name = 'activos/equipofuncional_confirm_delete.html'
    permission_required = 'activos.delete_equipofuncional'
    success_url = reverse_lazy('activos:equipofuncional_list')


# =============================================================================
# API AJAX
# =============================================================================

def get_niveles_by_planta(request):
    """Retorna los niveles de una planta en formato JSON."""
    planta_id = request.GET.get('planta_id')
    if planta_id:
        from apps.organizacion.models import Nivel
        niveles = Nivel.objects.filter(planta_id=planta_id, activo=True).values('id', 'nombre')
        return JsonResponse(list(niveles), safe=False)
    return JsonResponse([], safe=False)


def get_areas_by_nivel(request):
    """Retorna las áreas de un nivel en formato JSON."""
    nivel_id = request.GET.get('nivel_id')
    if nivel_id:
        from apps.organizacion.models import Area
        areas = Area.objects.filter(nivel_id=nivel_id, activa=True).values('id', 'nombre')
        return JsonResponse(list(areas), safe=False)
    return JsonResponse([], safe=False)


def get_subareas_by_area(request):
    """Retorna las subáreas de un área en formato JSON."""
    area_id = request.GET.get('area_id')
    if area_id:
        from apps.organizacion.models import SubArea
        subareas = SubArea.objects.filter(area_id=area_id, activa=True).values('id', 'nombre')
        return JsonResponse(list(subareas), safe=False)
    return JsonResponse([], safe=False)
