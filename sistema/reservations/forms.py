from reservations.models import *
from django import forms

class HourForm(forms.ModelForm):
    class Meta:

        model = Hour
        fields = ['range_hour']
        labels = {
            'range_hour': 'Siga o exemplo de horário:',
        }
        widgets = {
            'range_hour': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Ex: 07:01 - 08:00",
                }
            ),
        }