from django import forms

from apps.accounts.models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'type', 'initial', 'subsidiary']
        labels = {
            'name': 'Descripcion',
            'type': 'Tipo',
            'initial': 'Inicial',
            'subsidiary': 'Sucursal'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Tipo',
                    'id': 'type',
                    'name': 'type',
                    'required': 'required'
                }
            ),
            'initial': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0.00',
                    'id': 'initial',
                    'name': 'initial',
                    'step': '1',
                    'min': '0',
                    'required': 'required'
                }
            ),
            'subsidiary': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Filial',
                    'id': 'subsidiary',
                    'name': 'subsidiary',
                    'required': 'required'
                }
            ),
        }
