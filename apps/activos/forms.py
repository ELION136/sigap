"""
Formularios para la app activos.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Fieldset
from .models import (
    TipoActivo, Estado, TipoPropiedad, 
    Activo, UbicacionActivo, EquipoFuncional
)


class TipoActivoForm(forms.ModelForm):
    """Formulario para el modelo TipoActivo."""
    
    class Meta:
        model = TipoActivo
        fields = [
            'codigo', 'nombre', 'descripcion', 'categoria',
            'vida_util_anios', 'depreciable', 'requiere_mantenimiento', 'activo'
        ]
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
                Column('categoria', css_class='md:w-1/2'),
                Column('vida_util_anios', css_class='md:w-1/2'),
            ),
            Row(
                Column('depreciable', css_class='md:w-1/3'),
                Column('requiere_mantenimiento', css_class='md:w-1/3'),
                Column('activo', css_class='md:w-1/3'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'activos:tipoactivo_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class EstadoForm(forms.ModelForm):
    """Formulario para el modelo Estado."""
    
    class Meta:
        model = Estado
        fields = [
            'codigo', 'nombre', 'descripcion', 'color',
            'operativo', 'orden', 'activo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='md:w-1/4'),
                Column('nombre', css_class='md:w-1/2'),
                Column('orden', css_class='md:w-1/4'),
            ),
            'descripcion',
            Row(
                Column('color', css_class='md:w-1/3'),
                Column('operativo', css_class='md:w-1/3'),
                Column('activo', css_class='md:w-1/3'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'activos:estado_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class TipoPropiedadForm(forms.ModelForm):
    """Formulario para el modelo TipoPropiedad."""
    
    class Meta:
        model = TipoPropiedad
        fields = ['codigo', 'nombre', 'descripcion', 'activo']
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
            'activo',
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'activos:tipopropiedad_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class UbicacionActivoForm(forms.ModelForm):
    """Formulario para el modelo UbicacionActivo."""
    
    class Meta:
        model = UbicacionActivo
        fields = [
            'planta', 'nivel', 'area', 'subarea', 'ubicacion_especifica'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'planta',
            'nivel',
            'area',
            'subarea',
            'ubicacion_especifica',
        )


class ActivoForm(forms.ModelForm):
    """Formulario para el modelo Activo."""
    
    # Campos de ubicación
    planta = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Planta'
    )
    nivel = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Nivel'
    )
    area = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Área'
    )
    subarea = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Subárea'
    )
    ubicacion_especifica = forms.CharField(
        required=False,
        label='Ubicación específica'
    )
    
    class Meta:
        model = Activo
        fields = [
            'codigo', 'codigo_interno', 'codigo_contable', 'nombre', 'descripcion',
            'tipo', 'estado', 'tipo_propiedad', 'responsable',
            'fecha_adquisicion', 'fecha_instalacion', 'fecha_garantia',
            'proveedor', 'numero_factura', 'costo_adquisicion', 'valor_actual', 'moneda',
            'marca', 'modelo', 'numero_serie', 'capacidad', 'dimensiones', 'peso',
            'imagen', 'manual', 'ficha_tecnica',
            'frecuencia_mantenimiento', 'notas'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_garantia': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar querysets para ubicación
        from apps.organizacion.models import Planta, Nivel, Area, SubArea
        self.fields['planta'].queryset = Planta.objects.filter(activa=True)
        self.fields['nivel'].queryset = Nivel.objects.filter(activo=True)
        self.fields['area'].queryset = Area.objects.filter(activa=True)
        self.fields['subarea'].queryset = SubArea.objects.filter(activa=True)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Fieldset(
                'Información General',
                Row(
                    Column('codigo', css_class='md:w-1/3'),
                    Column('nombre', css_class='md:w-2/3'),
                ),
                Row(
                    Column('codigo_interno', css_class='md:w-1/2'),
                    Column('codigo_contable', css_class='md:w-1/2'),
                ),
                'descripcion',
            ),
            Fieldset(
                'Clasificación',
                Row(
                    Column('tipo', css_class='md:w-1/3'),
                    Column('estado', css_class='md:w-1/3'),
                    Column('tipo_propiedad', css_class='md:w-1/3'),
                ),
            ),
            Fieldset(
                'Ubicación',
                Row(
                    Column('planta', css_class='md:w-1/2'),
                    Column('nivel', css_class='md:w-1/2'),
                ),
                Row(
                    Column('area', css_class='md:w-1/2'),
                    Column('subarea', css_class='md:w-1/2'),
                ),
                'ubicacion_especifica',
                'responsable',
            ),
            Fieldset(
                'Adquisición',
                Row(
                    Column('fecha_adquisicion', css_class='md:w-1/3'),
                    Column('fecha_instalacion', css_class='md:w-1/3'),
                    Column('fecha_garantia', css_class='md:w-1/3'),
                ),
                Row(
                    Column('proveedor', css_class='md:w-1/2'),
                    Column('numero_factura', css_class='md:w-1/2'),
                ),
                Row(
                    Column('costo_adquisicion', css_class='md:w-1/3'),
                    Column('valor_actual', css_class='md:w-1/3'),
                    Column('moneda', css_class='md:w-1/3'),
                ),
            ),
            Fieldset(
                'Especificaciones Técnicas',
                Row(
                    Column('marca', css_class='md:w-1/3'),
                    Column('modelo', css_class='md:w-1/3'),
                    Column('numero_serie', css_class='md:w-1/3'),
                ),
                Row(
                    Column('capacidad', css_class='md:w-1/3'),
                    Column('dimensiones', css_class='md:w-1/3'),
                    Column('peso', css_class='md:w-1/3'),
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Archivos',
                Row(
                    Column('imagen', css_class='md:w-1/3'),
                    Column('manual', css_class='md:w-1/3'),
                    Column('ficha_tecnica', css_class='md:w-1/3'),
                ),
                Div(
                    HTML('{% if object.imagen %}<img src="{{ object.imagen.url }}" class="mt-2 max-h-48 object-cover rounded-lg" />{% endif %}'),
                    css_class='mb-4'
                ),
                css_class='collapse'
            ),
            Fieldset(
                'Mantenimiento',
                'frecuencia_mantenimiento',
                css_class='collapse'
            ),
            Fieldset(
                'Notas',
                'notas',
                css_class='collapse'
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'activos:activo_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            
            # Crear o actualizar ubicación
            if self.cleaned_data.get('planta') and self.cleaned_data.get('nivel') and self.cleaned_data.get('area'):
                ubicacion, created = UbicacionActivo.objects.update_or_create(
                    activo=instance,
                    actual=True,
                    defaults={
                        'planta': self.cleaned_data['planta'],
                        'nivel': self.cleaned_data['nivel'],
                        'area': self.cleaned_data['area'],
                        'subarea': self.cleaned_data.get('subarea'),
                        'ubicacion_especifica': self.cleaned_data.get('ubicacion_especifica', ''),
                    }
                )
                instance.ubicacion = ubicacion
                instance.save(update_fields=['ubicacion'])
        
        return instance


class ActivoEstadoForm(forms.ModelForm):
    """Formulario simplificado para cambiar solo el estado del activo."""
    
    class Meta:
        model = Activo
        fields = ['estado', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Motivo del cambio de estado...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'estado',
            'notas',
            Div(
                Submit('submit', 'Guardar Cambio', css_class='btn-primary'),
                css_class='flex justify-end mt-4'
            )
        )


class EquipoFuncionalForm(forms.ModelForm):
    """Formulario para el modelo EquipoFuncional."""
    
    class Meta:
        model = EquipoFuncional
        fields = [
            'codigo', 'nombre', 'descripcion', 'activos',
            'responsable', 'area', 'estado_operativo', 'criticidad',
            'fecha_instalacion', 'imagen', 'documentacion', 'notas', 'activo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('nombre', css_class='md:w-2/3'),
            ),
            'descripcion',
            'activos',
            Row(
                Column('responsable', css_class='md:w-1/2'),
                Column('area', css_class='md:w-1/2'),
            ),
            Row(
                Column('estado_operativo', css_class='md:w-1/2'),
                Column('criticidad', css_class='md:w-1/2'),
            ),
            'fecha_instalacion',
            Row(
                Column('imagen', css_class='md:w-1/2'),
                Column('documentacion', css_class='md:w-1/2'),
            ),
            Div(
                HTML('{% if object.imagen %}<img src="{{ object.imagen.url }}" class="mt-2 max-h-48 object-cover rounded-lg" />{% endif %}'),
                css_class='mb-4'
            ),
            'notas',
            'activo',
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'activos:equipofuncional_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )
