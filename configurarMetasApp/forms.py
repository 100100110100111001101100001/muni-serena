from django import forms


class PeriodoForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre del período',
        min_length=3,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Evaluación anual 2026',
        }),
    )


class ItemForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre del ítem',
        min_length=3,
        max_length=120,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej. Cumplimiento de compromisos',
        }),
    )
    meta = forms.DecimalField(
        label='Meta numérica',
        min_value=0,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
            'step': '0.01',
            'min': '0',
        }),
    )
    ponderacion = forms.DecimalField(
        label='Ponderación (%)',
        min_value=0,
        max_value=100,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0',
            'step': '0.01',
            'min': '0',
            'max': '100',
        }),
    )
