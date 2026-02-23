"""
Vistas para la app reportes del proyecto SIGAP.
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta, datetime

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from apps.activos.models import Activo, TipoActivo, Estado, EquipoFuncional
from apps.mantenimiento.models import Mantenimiento
from apps.organizacion.models import Planta, Area, Responsable


class ReporteIndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """Vista principal de reportes."""
    template_name = 'reportes/index.html'
    permission_required = 'reportes.view_reporte'


@login_required
@permission_required('reportes.view_reporte')
def reporte_activos(request):
    """Genera reporte de activos con filtros."""
    # Filtros
    planta_id = request.GET.get('planta')
    tipo_id = request.GET.get('tipo')
    estado_id = request.GET.get('estado')
    responsable_id = request.GET.get('responsable')
    
    queryset = Activo.objects.select_related(
        'tipo', 'estado', 'tipo_propiedad', 'responsable', 'ubicacion'
    )
    
    if planta_id:
        queryset = queryset.filter(ubicacion__planta_id=planta_id)
    if tipo_id:
        queryset = queryset.filter(tipo_id=tipo_id)
    if estado_id:
        queryset = queryset.filter(estado_id=estado_id)
    if responsable_id:
        queryset = queryset.filter(responsable_id=responsable_id)
    
    # Estadísticas
    stats = {
        'total': queryset.count(),
        'por_tipo': queryset.values('tipo__nombre').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'por_estado': queryset.values('estado__nombre', 'estado__color').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'por_planta': queryset.values('ubicacion__planta__nombre').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'valor_total': queryset.aggregate(
            total=Sum('valor_actual')
        )['total'] or 0,
    }
    
    context = {
        'activos': queryset[:100],  # Limitar a 100 para la vista
        'stats': stats,
        'plantas': Planta.objects.filter(activa=True),
        'tipos': TipoActivo.objects.filter(activo=True),
        'estados': Estado.objects.filter(activo=True),
        'responsables': Responsable.objects.filter(activo=True),
        'filtros': {
            'planta': planta_id,
            'tipo': tipo_id,
            'estado': estado_id,
            'responsable': responsable_id,
        }
    }
    return render(request, 'reportes/reporte_activos.html', context)


@login_required
@permission_required('reportes.view_reporte')
def reporte_mantenimientos(request):
    """Genera reporte de mantenimientos."""
    # Filtros de fecha
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    tipo = request.GET.get('tipo')
    estado = request.GET.get('estado')
    
    if not fecha_desde:
        fecha_desde = (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not fecha_hasta:
        fecha_hasta = timezone.now().strftime('%Y-%m-%d')
    
    queryset = Mantenimiento.objects.filter(
        fecha__gte=fecha_desde,
        fecha__lte=fecha_hasta
    ).select_related('activo', 'solicitado_por', 'realizado_por')
    
    if tipo:
        queryset = queryset.filter(tipo=tipo)
    if estado:
        queryset = queryset.filter(estado=estado)
    
    # Estadísticas
    stats = {
        'total': queryset.count(),
        'por_tipo': queryset.values('tipo').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'por_estado': queryset.values('estado').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'costo_total': queryset.aggregate(
            total=Sum('costo_total')
        )['total'] or 0,
        'tiempo_total': queryset.aggregate(
            total=Sum('tiempo_real')
        )['total'] or 0,
    }
    
    context = {
        'mantenimientos': queryset[:100],
        'stats': stats,
        'tipos': Mantenimiento.TIPO_MANTENIMIENTO,
        'estados': Mantenimiento.ESTADO_MANTENIMIENTO,
        'filtros': {
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
            'tipo': tipo,
            'estado': estado,
        }
    }
    return render(request, 'reportes/reporte_mantenimientos.html', context)


@login_required
@permission_required('reportes.view_reporte')
def reporte_equipos(request):
    """Genera reporte de equipos funcionales."""
    queryset = EquipoFuncional.objects.select_related(
        'area__nivel__planta', 'responsable'
    ).annotate(activos_count=Count('activos'))
    
    # Estadísticas
    stats = {
        'total': queryset.count(),
        'por_estado': queryset.values('estado_operativo').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'por_criticidad': queryset.values('criticidad').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
        'por_planta': queryset.values('area__nivel__planta__nombre').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad'),
    }
    
    context = {
        'equipos': queryset[:100],
        'stats': stats,
    }
    return render(request, 'reportes/reporte_equipos.html', context)


# =============================================================================
# EXPORTACIONES A EXCEL
# =============================================================================

def crear_estilos_excel():
    """Crea estilos comunes para archivos Excel."""
    estilos = {
        'header': Font(bold=True, color='FFFFFF', size=11),
        'header_fill': PatternFill(start_color='2563EB', end_color='2563EB', fill_type='solid'),
        'border': Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        ),
        'center': Alignment(horizontal='center', vertical='center'),
        'left': Alignment(horizontal='left', vertical='center'),
    }
    return estilos


@login_required
@permission_required('reportes.view_reporte')
def exportar_activos_excel(request):
    """Exporta activos a Excel."""
    # Crear workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Activos"
    
    estilos = crear_estilos_excel()
    
    # Headers
    headers = [
        'Código', 'Nombre', 'Tipo', 'Estado', 'Propiedad',
        'Planta', 'Nivel', 'Área', 'Responsable',
        'Marca', 'Modelo', 'No. Serie',
        'Fecha Adquisición', 'Costo', 'Valor Actual'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = estilos['header']
        cell.fill = estilos['header_fill']
        cell.alignment = estilos['center']
        cell.border = estilos['border']
    
    # Datos
    activos = Activo.objects.select_related(
        'tipo', 'estado', 'tipo_propiedad', 'responsable', 'ubicacion'
    )
    
    for row, activo in enumerate(activos, 2):
        ws.cell(row=row, column=1, value=activo.codigo)
        ws.cell(row=row, column=2, value=activo.nombre)
        ws.cell(row=row, column=3, value=activo.tipo.nombre if activo.tipo else '')
        ws.cell(row=row, column=4, value=activo.estado.nombre if activo.estado else '')
        ws.cell(row=row, column=5, value=activo.tipo_propiedad.nombre if activo.tipo_propiedad else '')
        ws.cell(row=row, column=6, value=activo.ubicacion.planta.nombre if activo.ubicacion else '')
        ws.cell(row=row, column=7, value=activo.ubicacion.nivel.nombre if activo.ubicacion else '')
        ws.cell(row=row, column=8, value=activo.ubicacion.area.nombre if activo.ubicacion else '')
        ws.cell(row=row, column=9, value=str(activo.responsable) if activo.responsable else '')
        ws.cell(row=row, column=10, value=activo.marca)
        ws.cell(row=row, column=11, value=activo.modelo)
        ws.cell(row=row, column=12, value=activo.numero_serie)
        ws.cell(row=row, column=13, value=activo.fecha_adquisicion)
        ws.cell(row=row, column=14, value=float(activo.costo_adquisicion) if activo.costo_adquisicion else 0)
        ws.cell(row=row, column=15, value=float(activo.valor_actual) if activo.valor_actual else 0)
    
    # Ajustar anchos
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    
    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=activos.xlsx'
    wb.save(response)
    return response


@login_required
@permission_required('reportes.view_reporte')
def exportar_mantenimientos_excel(request):
    """Exporta mantenimientos a Excel."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Mantenimientos"
    
    estilos = crear_estilos_excel()
    
    headers = [
        'Código', 'Activo', 'Tipo', 'Fecha', 'Estado', 'Prioridad',
        'Descripción', 'Realizado por', 'Costo Total', 'Tiempo Real'
    ]
    
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = estilos['header']
        cell.fill = estilos['header_fill']
        cell.alignment = estilos['center']
        cell.border = estilos['border']
    
    mantenimientos = Mantenimiento.objects.select_related(
        'activo', 'realizado_por'
    )
    
    for row, mtto in enumerate(mantenimientos, 2):
        ws.cell(row=row, column=1, value=mtto.codigo)
        ws.cell(row=row, column=2, value=str(mtto.activo))
        ws.cell(row=row, column=3, value=mtto.get_tipo_display())
        ws.cell(row=row, column=4, value=mtto.fecha)
        ws.cell(row=row, column=5, value=mtto.get_estado_display())
        ws.cell(row=row, column=6, value=mtto.get_prioridad_display())
        ws.cell(row=row, column=7, value=mtto.descripcion)
        ws.cell(row=row, column=8, value=str(mtto.realizado_por) if mtto.realizado_por else '')
        ws.cell(row=row, column=9, value=float(mtto.costo_total) if mtto.costo_total else 0)
        ws.cell(row=row, column=10, value=float(mtto.tiempo_real) if mtto.tiempo_real else 0)
    
    for col in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 18
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=mantenimientos.xlsx'
    wb.save(response)
    return response


# =============================================================================
# DASHBOARD API
# =============================================================================

@login_required
def dashboard_data(request):
    """Retorna datos para el dashboard en formato JSON."""
    from django.http import JsonResponse
    
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)
    
    data = {
        'activos': {
            'total': Activo.objects.count(),
            'operativos': Activo.objects.filter(estado__operativo=True).count(),
            'fuera_servicio': Activo.objects.filter(estado__operativo=False).count(),
        },
        'mantenimientos': {
            'pendientes': Mantenimiento.objects.filter(estado='PENDIENTE').count(),
            'completados_mes': Mantenimiento.objects.filter(
                estado='COMPLETADO',
                fecha_realizacion__month=hoy.month,
                fecha_realizacion__year=hoy.year
            ).count(),
            'vencidos': Mantenimiento.objects.filter(
                estado='PENDIENTE',
                fecha__lt=hoy
            ).count(),
        },
        'equipos': {
            'total': EquipoFuncional.objects.count(),
            'operativos': EquipoFuncional.objects.filter(estado_operativo='OPERATIVO').count(),
        },
        'activos_por_tipo': list(Activo.objects.values('tipo__nombre').annotate(
            cantidad=Count('id')
        ).order_by('-cantidad')[:5]),
        'mantenimientos_por_mes': list(Mantenimiento.objects.filter(
            fecha__gte=hace_30_dias
        ).values('fecha__month').annotate(
            cantidad=Count('id')
        ).order_by('fecha__month')),
    }
    
    return JsonResponse(data)
