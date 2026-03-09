"""
Vistas para la app mantenimiento del proyecto SIGAP.
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count, Sum
from django.utils import timezone

from .models import TipoMantenimiento, Mantenimiento, RepuestoUtilizado
from .forms import (
    TipoMantenimientoForm, MantenimientoForm,
    MantenimientoQuickForm, RepuestoUtilizadoForm,
)
from apps.activos.models import Activo


# ─── Mixins base ───────────────────────────────────────────────────────────────

class AuthMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Login + permiso en un solo mixin."""


class BaseCreateView(SuccessMessageMixin, AuthMixin, CreateView):
    def form_valid(self, form):
        if hasattr(form.instance, 'creado_por'):
            form.instance.creado_por = self.request.user
        if hasattr(form.instance, 'modificado_por'):
            form.instance.modificado_por = self.request.user
        return super().form_valid(form)


class BaseUpdateView(SuccessMessageMixin, AuthMixin, UpdateView):
    def form_valid(self, form):
        if hasattr(form.instance, 'modificado_por'):
            form.instance.modificado_por = self.request.user
        return super().form_valid(form)


class BaseDeleteView(AuthMixin, DeleteView):
    def form_valid(self, form):
        messages.success(
            self.request,
            f'{self.model._meta.verbose_name} eliminado exitosamente.'
        )
        return super().form_valid(form)


# ─── TipoMantenimiento ──────────────────────────────────────────────────────────

class TipoMantenimientoListView(AuthMixin, ListView):
    model = TipoMantenimiento
    template_name = 'mantenimiento/tipomantenimiento_list.html'
    context_object_name = 'tipos'
    permission_required = 'mantenimiento.view_tipomantenimiento'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().annotate(
            total_mantenimientos=Count('mantenimiento')
        )
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(codigo__icontains=q) | Q(nombre__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Tipos de Mantenimiento'
        ctx['search_query'] = self.request.GET.get('q', '')
        return ctx


class TipoMantenimientoDetailView(AuthMixin, DetailView):
    model = TipoMantenimiento
    template_name = 'mantenimiento/tipomantenimiento_detail.html'
    context_object_name = 'tipo'
    permission_required = 'mantenimiento.view_tipomantenimiento'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = str(self.object)
        ctx['mantenimientos'] = (
            self.object.mantenimiento_set
            .select_related('activo')
            .order_by('-fecha')[:10]
        )
        return ctx


class TipoMantenimientoCreateView(BaseCreateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'mantenimiento/tipomantenimiento_form.html'
    permission_required = 'mantenimiento.add_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')
    success_message = 'Tipo de mantenimiento creado exitosamente.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Nuevo Tipo de Mantenimiento'
        ctx['action'] = 'crear'
        return ctx


class TipoMantenimientoUpdateView(BaseUpdateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'mantenimiento/tipomantenimiento_form.html'
    permission_required = 'mantenimiento.change_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')
    success_message = 'Tipo de mantenimiento actualizado exitosamente.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Editar: {self.object}'
        ctx['action'] = 'editar'
        return ctx


class TipoMantenimientoDeleteView(BaseDeleteView):
    model = TipoMantenimiento
    template_name = 'mantenimiento/confirm_delete.html'
    permission_required = 'mantenimiento.delete_tipomantenimiento'
    success_url = reverse_lazy('mantenimiento:tipomantenimiento_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Eliminar Tipo de Mantenimiento'
        ctx['cancel_url'] = reverse_lazy('mantenimiento:tipomantenimiento_list')
        return ctx


# ─── Mantenimiento ──────────────────────────────────────────────────────────────

class MantenimientoListView(AuthMixin, ListView):
    model = Mantenimiento
    template_name = 'mantenimiento/mantenimiento_list.html'
    context_object_name = 'mantenimientos'
    permission_required = 'mantenimiento.view_mantenimiento'
    paginate_by = 25

    def get_queryset(self):
        qs = Mantenimiento.objects.select_related(
            'activo', 'solicitado_por', 'realizado_por'
        )
        f = self.request.GET

        q           = f.get('q', '').strip()
        tipo        = f.get('tipo', '')
        estado      = f.get('estado', '')
        prioridad   = f.get('prioridad', '')
        activo_id   = f.get('activo', '')
        fecha_desde = f.get('fecha_desde', '')
        fecha_hasta = f.get('fecha_hasta', '')

        if q:
            qs = qs.filter(
                Q(codigo__icontains=q) |
                Q(descripcion__icontains=q) |
                Q(activo__nombre__icontains=q) |
                Q(activo__codigo__icontains=q)
            )
        if tipo:
            qs = qs.filter(tipo=tipo)
        if estado:
            qs = qs.filter(estado=estado)
        if prioridad:
            qs = qs.filter(prioridad=prioridad)
        if activo_id:
            qs = qs.filter(activo_id=activo_id)
        if fecha_desde:
            qs = qs.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha__lte=fecha_hasta)

        return qs.order_by('-fecha')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Mantenimientos'

        # Opciones para los selects del filtro
        ctx['tipo_choices']      = Mantenimiento.TIPO_MANTENIMIENTO
        ctx['estado_choices']    = Mantenimiento.ESTADO_MANTENIMIENTO
        ctx['prioridad_choices'] = Mantenimiento.PRIORIDAD
        ctx['activos']           = Activo.objects.filter(activo_registro=True).only('id', 'nombre')

        # Filtros activos (para repoblar el formulario y paginación)
        ctx['filtros'] = {k: self.request.GET.get(k, '') for k in (
            'q', 'tipo', 'estado', 'prioridad', 'activo', 'fecha_desde', 'fecha_hasta'
        )}

        # KPIs
        hoy  = timezone.now().date()
        base = Mantenimiento.objects
        ctx['kpi'] = {
            'total':           base.count(),
            'pendiente':       base.filter(estado='PENDIENTE').count(),
            'en_progreso':     base.filter(estado='EN_PROGRESO').count(),
            'completado':      base.filter(estado='COMPLETADO').count(),
            'vencidos':        base.filter(estado='PENDIENTE', fecha__lt=hoy).count(),
            'completados_mes': base.filter(
                estado='COMPLETADO',
                fecha_realizacion__month=hoy.month,
                fecha_realizacion__year=hoy.year,
            ).count(),
        }
        return ctx


class MantenimientoDetailView(AuthMixin, DetailView):
    model = Mantenimiento
    template_name = 'mantenimiento/mantenimiento_detail.html'
    context_object_name = 'mnt'
    permission_required = 'mantenimiento.view_mantenimiento'

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('activo', 'solicitado_por', 'realizado_por')
            .prefetch_related('repuestos')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = str(self.object)
        ctx['repuestos'] = self.object.repuestos.all()
        ctx['costo_repuestos_total'] = (
            self.object.repuestos.aggregate(t=Sum('costo_total'))['t'] or 0
        )
        ctx['historial'] = (
            Mantenimiento.objects
            .filter(activo=self.object.activo)
            .exclude(pk=self.object.pk)
            .order_by('-fecha')[:5]
        )
        return ctx


class MantenimientoCreateView(BaseCreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'mantenimiento/mantenimiento_form.html'
    permission_required = 'mantenimiento.add_mantenimiento'
    success_message = 'Mantenimiento registrado exitosamente.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Registrar Mantenimiento'
        ctx['action'] = 'crear'
        return ctx


class MantenimientoUpdateView(BaseUpdateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'mantenimiento/mantenimiento_form.html'
    permission_required = 'mantenimiento.change_mantenimiento'
    success_message = 'Mantenimiento actualizado exitosamente.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Editar: {self.object}'
        ctx['action'] = 'editar'
        return ctx


class MantenimientoDeleteView(BaseDeleteView):
    model = Mantenimiento
    template_name = 'mantenimiento/confirm_delete.html'
    permission_required = 'mantenimiento.delete_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Eliminar Mantenimiento'
        ctx['cancel_url'] = self.object.get_absolute_url()
        return ctx


class MantenimientoQuickCreateView(SuccessMessageMixin, AuthMixin, CreateView):
    model = Mantenimiento
    form_class = MantenimientoQuickForm
    template_name = 'mantenimiento/mantenimiento_quick_form.html'
    permission_required = 'mantenimiento.add_mantenimiento'
    success_url = reverse_lazy('mantenimiento:mantenimiento_list')
    success_message = 'Mantenimiento creado exitosamente.'

    def form_valid(self, form):
        if hasattr(form.instance, 'creado_por'):
            form.instance.creado_por = self.request.user
        if hasattr(form.instance, 'modificado_por'):
            form.instance.modificado_por = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Registro Rápido'
        return ctx


# ─── RepuestoUtilizado ──────────────────────────────────────────────────────────

class RepuestoUtilizadoCreateView(SuccessMessageMixin, AuthMixin, CreateView):
    model = RepuestoUtilizado
    form_class = RepuestoUtilizadoForm
    template_name = 'mantenimiento/repuesto_form.html'
    permission_required = 'mantenimiento.add_repuestoutilizado'
    success_message = 'Repuesto agregado exitosamente.'

    def dispatch(self, request, *args, **kwargs):
        self.mantenimiento = get_object_or_404(Mantenimiento, pk=kwargs['mantenimiento_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.mantenimiento = self.mantenimiento
        if hasattr(form.instance, 'creado_por'):
            form.instance.creado_por = self.request.user
        if hasattr(form.instance, 'modificado_por'):
            form.instance.modificado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.mantenimiento.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mantenimiento'] = self.mantenimiento
        ctx['page_title'] = 'Agregar Repuesto'
        ctx['action'] = 'crear'
        return ctx


class RepuestoUtilizadoUpdateView(SuccessMessageMixin, AuthMixin, UpdateView):
    model = RepuestoUtilizado
    form_class = RepuestoUtilizadoForm
    template_name = 'mantenimiento/repuesto_form.html'
    permission_required = 'mantenimiento.change_repuestoutilizado'
    success_message = 'Repuesto actualizado exitosamente.'

    def form_valid(self, form):
        if hasattr(form.instance, 'modificado_por'):
            form.instance.modificado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.mantenimiento.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mantenimiento'] = self.object.mantenimiento
        ctx['page_title'] = 'Editar Repuesto'
        ctx['action'] = 'editar'
        return ctx


class RepuestoUtilizadoDeleteView(AuthMixin, DeleteView):
    model = RepuestoUtilizado
    template_name = 'mantenimiento/confirm_delete.html'
    permission_required = 'mantenimiento.delete_repuestoutilizado'

    def form_valid(self, form):
        messages.success(self.request, 'Repuesto eliminado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.mantenimiento.get_absolute_url()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Eliminar Repuesto'
        ctx['cancel_url'] = self.object.mantenimiento.get_absolute_url()
        return ctx
