from django import forms

from apps.clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['document', 'first_name', 'last_name', 'phone', 'address']
        labels = {
            'document': 'Documento',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'phone': 'Celular',
            'address': 'Direccion'
        }
        widgets = {
            'document': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Documento',
                    'id': 'document',
                    'name': 'document',
                    'required': 'required'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombres',
                    'id': 'first_name',
                    'name': 'first_name',
                    'required': 'required'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos',
                    'id': 'last_name',
                    'name': 'last_name'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Celular',
                    'id': 'phone',
                    'name': 'phone'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Direccion',
                    'id': 'address',
                    'name': 'address'
                }
            )
        }
