"""
Formularios para la app mantenimiento.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Fieldset
from .models import TipoMantenimiento, Mantenimiento, RepuestoUtilizado


class TipoMantenimientoForm(forms.ModelForm):
    """Formulario para el modelo TipoMantenimiento."""
    
    class Meta:
        model = TipoMantenimiento
        fields = ['codigo', 'nombre', 'descripcion', 'color', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('nombre', css_class='md:w-2/3'),
            ),
            'descripcion',
            Row(
                Column('color', css_class='md:w-1/2'),
                Column('activo', css_class='md:w-1/2'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'mantenimiento:tipomantenimiento_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class MantenimientoForm(forms.ModelForm):
    """Formulario para el modelo Mantenimiento."""
    
    class Meta:
        model = Mantenimiento
        fields = [
            'activo', 'tipo', 'codigo', 'fecha', 'estado', 'prioridad',
            'descripcion', 'trabajo_realizado',
            'solicitado_por', 'realizado_por',
            'costo_mano_obra', 'costo_repuestos', 'moneda',
            'tiempo_estimado', 'tiempo_real', 'fecha_realizacion',
            'resultado', 'proximo_mantenimiento',
            'evidencia_fotografica', 'documento',
            'observaciones', 'recomendaciones'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'trabajo_realizado': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
            'recomendaciones': forms.Textarea(attrs={'rows': 2}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'fecha_realizacion': forms.DateInput(attrs={'type': 'date'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Información General',
                Row(
                    Column('activo', css_class='md:w-1/2'),
                    Column('tipo', css_class='md:w-1/2'),
                ),
                Row(
                    Column('codigo', css_class='md:w-1/3'),
                    Column('fecha', css_class='md:w-1/3'),
                    Column('estado', css_class='md:w-1/3'),
                ),
                'prioridad',
            ),
            Fieldset(
                'Descripción del Trabajo',
                'descripcion',
                'trabajo_realizado',
            ),
            Fieldset(
                'Personal',
                Row(
                    Column('solicitado_por', css_class='md:w-1/2'),
                    Column('realizado_por', css_class='md:w-1/2'),
                ),
            ),
            Fieldset(
                'Costos',
                Row(
                    Column('costo_mano_obra', css_class='md:w-1/3'),
                    Column('costo_repuestos', css_class='md:w-1/3'),
                    Column('moneda', css_class='md:w-1/3'),
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Tiempo',
                Row(
                    Column('tiempo_estimado', css_class='md:w-1/3'),
                    Column('tiempo_real', css_class='md:w-1/3'),
                    Column('fecha_realizacion', css_class='md:w-1/3'),
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Resultado',
                Row(
                    Column('resultado', css_class='md:w-1/2'),
                    Column('proximo_mantenimiento', css_class='md:w-1/2'),
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Documentación',
                Row(
                    Column('evidencia_fotografica', css_class='md:w-1/2'),
                    Column('documento', css_class='md:w-1/2'),
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Notas',
                'observaciones',
                'recomendaciones',
                css_class='collapse'
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'mantenimiento:mantenimiento_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class MantenimientoQuickForm(forms.ModelForm):
    """Formulario rápido para crear mantenimientos básicos."""
    
    class Meta:
        model = Mantenimiento
        fields = ['activo', 'tipo', 'fecha', 'prioridad', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'activo',
            Row(
                Column('tipo', css_class='md:w-1/2'),
                Column('prioridad', css_class='md:w-1/2'),
            ),
            'fecha',
            'descripcion',
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                css_class='flex justify-end mt-4'
            )
        )


class RepuestoUtilizadoForm(forms.ModelForm):
    """Formulario para el modelo RepuestoUtilizado."""
    
    class Meta:
        model = RepuestoUtilizado
        fields = [
            'codigo', 'descripcion', 'cantidad', 'unidad',
            'costo_unitario', 'proveedor', 'notas'
        ]
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('descripcion', css_class='md:w-2/3'),
            ),
            Row(
                Column('cantidad', css_class='md:w-1/3'),
                Column('unidad', css_class='md:w-1/3'),
                Column('costo_unitario', css_class='md:w-1/3'),
            ),
            'proveedor',
            'notas',
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                css_class='flex justify-end mt-4'
            )
        )
