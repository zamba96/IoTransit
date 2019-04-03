from django import forms
from .models import Registro


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = [

            'id',
            'fecha',
            'lectura',
        ]
        labels = {
            'id': 'Id',
            'fecha': 'Fecha',
            'lectura': 'Lectura',
        }
