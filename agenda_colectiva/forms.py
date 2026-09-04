from django import forms
from ficha_desempeno.services import FuncionariosService


class CompromisoForm(forms.Form):
    vecino = forms.CharField(
        label="Nombre del Vecino Solicitante",
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Juan Pérez'})
    )
    telefono = forms.CharField(
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. +56912345678'})
    )
    territorio = forms.ChoiceField(
        label="Territorio / Delegación",
        choices=[
            ('Centro', 'Centro'),
            ('Rural', 'Rural'),
            ('Las Compañías', 'Las Compañías'),
            ('La Pampa', 'La Pampa'),
            ('La Antena - La Florida', 'La Antena - La Florida'),
            ('Avenida del Mar', 'Avenida del Mar')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    descripcion = forms.CharField(
        label="Descripción del Requerimiento",
        min_length=10,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Explique claramente el compromiso...'})
    )
    fecha_compromiso = forms.DateField(
        label="Fecha Límite de Compromiso",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    responsable_id = forms.ChoiceField(
        label="Funcionario Responsable Asignado",
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargamos los responsables de manera dinamica llamando a la API de tu compañero
        funcionarios = FuncionariosService.get_all()
        self.fields['responsable_id'].choices = [(f['id'], f['nombre']) for f in funcionarios]

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.startswith('+569') and len(telefono) < 9:
            raise forms.ValidationError("Ingrese un formato telefónico móvil chileno válido (+569XXXXXXXX).")
        return telefono
