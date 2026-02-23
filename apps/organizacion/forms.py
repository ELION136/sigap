"""
Formularios para la app organizacion.
"""
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from .models import Planta, Nivel, Area, SubArea, Responsable


class PlantaForm(forms.ModelForm):
    """Formulario para el modelo Planta."""
    
    class Meta:
        model = Planta
        fields = [
            'codigo', 'nombre', 'descripcion', 'direccion', 
            'ciudad', 'estado_provincia', 'codigo_postal', 'pais',
            'telefono', 'email', 'latitud', 'longitud', 
            'activa', 'imagen'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'latitud': forms.NumberInput(attrs={'step': '0.00000001'}),
            'longitud': forms.NumberInput(attrs={'step': '0.00000001'}),
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
            Row(
                Column('direccion', css_class='md:w-full'),
            ),
            Row(
                Column('ciudad', css_class='md:w-1/3'),
                Column('estado_provincia', css_class='md:w-1/3'),
                Column('codigo_postal', css_class='md:w-1/6'),
                Column('pais', css_class='md:w-1/6'),
            ),
            Row(
                Column('telefono', css_class='md:w-1/2'),
                Column('email', css_class='md:w-1/2'),
            ),
            Row(
                Column('latitud', css_class='md:w-1/2'),
                Column('longitud', css_class='md:w-1/2'),
            ),
            Row(
                Column('activa', css_class='md:w-1/2'),
                Column('imagen', css_class='md:w-1/2'),
            ),
            Div(
                HTML('<img id="imagen-preview" src="" class="mt-2 max-h-48 object-cover rounded-lg {{ object.imagen|yesno:\'block,hidden\' }}" />'),
                css_class='mb-4'
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'organizacion:planta_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class NivelForm(forms.ModelForm):
    """Formulario para el modelo Nivel."""
    
    class Meta:
        model = Nivel
        fields = [
            'planta', 'codigo', 'nombre', 'descripcion',
            'numero_nivel', 'altura', 'activo', 'plano'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'planta',
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('nombre', css_class='md:w-2/3'),
            ),
            'descripcion',
            Row(
                Column('numero_nivel', css_class='md:w-1/2'),
                Column('altura', css_class='md:w-1/2'),
            ),
            Row(
                Column('activo', css_class='md:w-1/2'),
                Column('plano', css_class='md:w-1/2'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'organizacion:nivel_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class AreaForm(forms.ModelForm):
    """Formulario para el modelo Area."""
    
    class Meta:
        model = Area
        fields = [
            'nivel', 'codigo', 'nombre', 'descripcion',
            'tipo_area', 'supervisor', 'activa', 'plano'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'nivel',
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('nombre', css_class='md:w-2/3'),
            ),
            'descripcion',
            Row(
                Column('tipo_area', css_class='md:w-1/2'),
                Column('supervisor', css_class='md:w-1/2'),
            ),
            Row(
                Column('activa', css_class='md:w-1/2'),
                Column('plano', css_class='md:w-1/2'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'organizacion:area_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class SubAreaForm(forms.ModelForm):
    """Formulario para el modelo SubArea."""
    
    class Meta:
        model = SubArea
        fields = [
            'area', 'codigo', 'nombre', 'descripcion',
            'responsable', 'activa'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'area',
            Row(
                Column('codigo', css_class='md:w-1/3'),
                Column('nombre', css_class='md:w-2/3'),
            ),
            'descripcion',
            Row(
                Column('responsable', css_class='md:w-1/2'),
                Column('activa', css_class='md:w-1/2'),
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'organizacion:subarea_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )


class ResponsableForm(forms.ModelForm):
    """Formulario para el modelo Responsable."""
    
    class Meta:
        model = Responsable
        fields = [
            'codigo', 'tipo', 'nombres', 'apellidos', 'foto',
            'puesto', 'departamento', 'fecha_ingreso',
            'email', 'telefono', 'telefono_movil', 'direccion',
            'usuario', 'activo', 'notas'
        ]
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'notas': forms.Textarea(attrs={'rows': 3}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='md:w-1/4'),
                Column('tipo', css_class='md:w-1/4'),
                Column('foto', css_class='md:w-1/2'),
            ),
            Row(
                Column('nombres', css_class='md:w-1/2'),
                Column('apellidos', css_class='md:w-1/2'),
            ),
            Row(
                Column('puesto', css_class='md:w-1/2'),
                Column('departamento', css_class='md:w-1/2'),
            ),
            'fecha_ingreso',
            Row(
                Column('email', css_class='md:w-1/2'),
                Column('telefono', css_class='md:w-1/4'),
                Column('telefono_movil', css_class='md:w-1/4'),
            ),
            'direccion',
            Row(
                Column('usuario', css_class='md:w-1/2'),
                Column('activo', css_class='md:w-1/2'),
            ),
            'notas',
            Div(
                Submit('submit', 'Guardar', css_class='btn-primary'),
                HTML('<a href="{% url \'organizacion:responsable_list\' %}" class="btn-secondary ml-2">Cancelar</a>'),
                css_class='flex justify-end mt-4'
            )
        )
