"""
Vistas para la app organizacion del proyecto SIGAP.
"""
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from django.db.models import Q

from .models import Planta, Nivel, Area, SubArea, Responsable
from .forms import PlantaForm, NivelForm, AreaForm, SubAreaForm, ResponsableForm


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
# VISTAS PARA PLANTA
# =============================================================================

class PlantaListView(BaseListView):
    """Vista de lista para Plantas."""
    model = Planta
    template_name = 'organizacion/planta_list.html'
    context_object_name = 'plantas'
    permission_required = 'organizacion.view_planta'


class PlantaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Planta."""
    model = Planta
    template_name = 'organizacion/planta_detail.html'
    context_object_name = 'planta'
    permission_required = 'organizacion.view_planta'


class PlantaCreateView(BaseCreateView):
    """Vista para crear Planta."""
    model = Planta
    form_class = PlantaForm
    template_name = 'organizacion/planta_form.html'
    permission_required = 'organizacion.add_planta'
    success_url = reverse_lazy('organizacion:planta_list')


class PlantaUpdateView(BaseUpdateView):
    """Vista para actualizar Planta."""
    model = Planta
    form_class = PlantaForm
    template_name = 'organizacion/planta_form.html'
    permission_required = 'organizacion.change_planta'
    success_url = reverse_lazy('organizacion:planta_list')


class PlantaDeleteView(BaseDeleteView):
    """Vista para eliminar Planta."""
    model = Planta
    template_name = 'organizacion/planta_confirm_delete.html'
    permission_required = 'organizacion.delete_planta'
    success_url = reverse_lazy('organizacion:planta_list')


# =============================================================================
# VISTAS PARA NIVEL
# =============================================================================

class NivelListView(BaseListView):
    """Vista de lista para Niveles."""
    model = Nivel
    template_name = 'organizacion/nivel/nivel_list.html'
    context_object_name = 'niveles'
    permission_required = 'organizacion.view_nivel'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        planta_id = self.request.GET.get('planta')
        if planta_id:
            queryset = queryset.filter(planta_id=planta_id)
        return queryset.select_related('planta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantas'] = Planta.objects.filter(activa=True)
        return context


class NivelDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Nivel."""
    model = Nivel
    template_name = 'organizacion/nivel/nivel_detail.html'
    context_object_name = 'nivel'
    permission_required = 'organizacion.view_nivel'


class NivelCreateView(BaseCreateView):
    """Vista para crear Nivel."""
    model = Nivel
    form_class = NivelForm
    template_name = 'organizacion/nivel/nivel_form.html'
    permission_required = 'organizacion.add_nivel'
    success_url = reverse_lazy('organizacion:nivel_list')


class NivelUpdateView(BaseUpdateView):
    """Vista para actualizar Nivel."""
    model = Nivel
    form_class = NivelForm
    template_name = 'organizacion/nivel/nivel_form.html'
    permission_required = 'organizacion.change_nivel'
    success_url = reverse_lazy('organizacion:nivel_list')


class NivelDeleteView(BaseDeleteView):
    """Vista para eliminar Nivel."""
    model = Nivel
    template_name = 'organizacion/nivel/nivel_confirm_delete.html'
    permission_required = 'organizacion.delete_nivel'
    success_url = reverse_lazy('organizacion:nivel_list')


# =============================================================================
# VISTAS PARA AREA
# =============================================================================

class AreaListView(BaseListView):
    """Vista de lista para Áreas."""
    model = Area
    template_name = 'organizacion/area/area_list.html'
    context_object_name = 'areas'
    permission_required = 'organizacion.view_area'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        planta_id = self.request.GET.get('planta')
        tipo = self.request.GET.get('tipo')
        if planta_id:
            queryset = queryset.filter(nivel__planta_id=planta_id)
        if tipo:
            queryset = queryset.filter(tipo_area=tipo)
        return queryset.select_related('nivel__planta', 'supervisor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plantas'] = Planta.objects.filter(activa=True)
        context['tipos_area'] = Area._meta.get_field('tipo_area').choices
        return context


class AreaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Área."""
    model = Area
    template_name = 'organizacion/area/area_detail.html'
    context_object_name = 'area'
    permission_required = 'organizacion.view_area'


class AreaCreateView(BaseCreateView):
    """Vista para crear Área."""
    model = Area
    form_class = AreaForm
    template_name = 'organizacion/area/area_form.html'
    permission_required = 'organizacion.add_area'
    success_url = reverse_lazy('organizacion:area_list')


class AreaUpdateView(BaseUpdateView):
    """Vista para actualizar Área."""
    model = Area
    form_class = AreaForm
    template_name = 'organizacion/area/area_form.html'
    permission_required = 'organizacion.change_area'
    success_url = reverse_lazy('organizacion:area_list')


class AreaDeleteView(BaseDeleteView):
    """Vista para eliminar Área."""
    model = Area
    template_name = 'organizacion/area/area_confirm_delete.html'
    permission_required = 'organizacion.delete_area'
    success_url = reverse_lazy('organizacion:area_list')


# =============================================================================
# VISTAS PARA SUBAREA
# =============================================================================

class SubAreaListView(BaseListView):
    """Vista de lista para Subáreas."""
    model = SubArea
    template_name = 'organizacion/subarea/subarea_list.html'
    context_object_name = 'subareas'
    permission_required = 'organizacion.view_subarea'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        area_id = self.request.GET.get('area')
        if area_id:
            queryset = queryset.filter(area_id=area_id)
        return queryset.select_related('area__nivel__planta', 'responsable')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Area.objects.filter(activa=True)
        return context


class SubAreaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Subárea."""
    model = SubArea
    template_name = 'organizacion/subarea/subarea_detail.html'
    context_object_name = 'subarea'
    permission_required = 'organizacion.view_subarea'


class SubAreaCreateView(BaseCreateView):
    """Vista para crear Subárea."""
    model = SubArea
    form_class = SubAreaForm
    template_name = 'organizacion/subarea/subarea_form.html'
    permission_required = 'organizacion.add_subarea'
    success_url = reverse_lazy('organizacion:subarea_list')


class SubAreaUpdateView(BaseUpdateView):
    """Vista para actualizar Subárea."""
    model = SubArea
    form_class = SubAreaForm
    template_name = 'organizacion/subarea/subarea_form.html'
    permission_required = 'organizacion.change_subarea'
    success_url = reverse_lazy('organizacion:subarea_list')


class SubAreaDeleteView(BaseDeleteView):
    """Vista para eliminar Subárea."""
    model = SubArea
    template_name = 'organizacion/subarea/subarea_confirm_delete.html'
    permission_required = 'organizacion.delete_subarea'
    success_url = reverse_lazy('organizacion:subarea_list')


# =============================================================================
# VISTAS PARA RESPONSABLE
# =============================================================================

class ResponsableListView(BaseListView):
    """Vista de lista para Responsables."""
    model = Responsable
    template_name = 'organizacion/responsable/responsable_list.html'
    context_object_name = 'responsables'
    permission_required = 'organizacion.view_responsable'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.GET.get('tipo')
        activo = self.request.GET.get('activo')
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if activo is not None:
            queryset = queryset.filter(activo=activo == 'true')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Responsable.TIPO_RESPONSABLE
        return context


class ResponsableDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Vista de detalle para Responsable."""
    model = Responsable
    template_name = 'organizacion/responsable/responsable_detail.html'
    context_object_name = 'responsable'
    permission_required = 'organizacion.view_responsable'


class ResponsableCreateView(BaseCreateView):
    """Vista para crear Responsable."""
    model = Responsable
    form_class = ResponsableForm
    template_name = 'organizacion/responsable/responsable_form.html'
    permission_required = 'organizacion.add_responsable'
    success_url = reverse_lazy('organizacion:responsable_list')


class ResponsableUpdateView(BaseUpdateView):
    """Vista para actualizar Responsable."""
    model = Responsable
    form_class = ResponsableForm
    template_name = 'organizacion/responsable/responsable_form.html'
    permission_required = 'organizacion.change_responsable'
    success_url = reverse_lazy('organizacion:responsable_list')


class ResponsableDeleteView(BaseDeleteView):
    """Vista para eliminar Responsable."""
    model = Responsable
    template_name = 'organizacion/responsable/responsable_confirm_delete.html'
    permission_required = 'organizacion.delete_responsable'
    success_url = reverse_lazy('organizacion:responsable_list')
