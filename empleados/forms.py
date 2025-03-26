from django import forms
from .models import Empleado, Tarea

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre_empleado', 'apellido_empleado', 'email_empleado', 
                 'edad_empleado', 'genero_empleado', 'salario_empleado', 'foto_empleado']
        widgets = {
            'nombre_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_empleado': forms.TextInput(attrs={'class': 'form-control'}),
            'email_empleado': forms.EmailInput(attrs={'class': 'form-control'}),
            'edad_empleado': forms.NumberInput(attrs={'class': 'form-control'}),
            'genero_empleado': forms.Select(attrs={'class': 'form-control'}),
            'salario_empleado': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto_empleado': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['empleado', 'titulo_tarea', 'descripcion_tarea', 'fecha_limite', 'estado_tarea']
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'titulo_tarea': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_tarea': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado_tarea': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'empleado': 'Seleccionar Programador',
            'titulo_tarea': 'Título de la Tarea',
            'descripcion_tarea': 'Descripción',
            'fecha_limite': 'Fecha Límite',
            'estado_tarea': 'Estado'
        } 