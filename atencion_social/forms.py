from django import forms


class CasoSocialForm(forms.Form):
    rut_vecino = forms.CharField(
        label="RUT del Beneficiario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12.345.678-9'})
    )
    nombre_vecino = forms.CharField(
        label="Nombre Completo",
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    direccion = forms.CharField(
        label="Dirección de Domicilio",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        label="Teléfono de Contacto",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean_rut_vecino(self):
        rut = self.cleaned_data.get('rut_vecino')
        return rut.replace(" ", "").upper()


class AtencionSecuencialForm(forms.Form):
    servicio = forms.CharField(
        label="Servicio o Ayuda Solicitada",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Canasta de alimentos...'})
    )
    observacion = forms.CharField(
        label="Observación Técnica / Seguimiento",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    resultado = forms.ChoiceField(
        label="Estatus del Logro",
        choices=[('Pendiente', 'Pendiente'), ('Completado', 'Completado')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
