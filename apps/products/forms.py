from django import forms
from django.forms import ChoiceField, RadioSelect

from apps.products.models import Product


class ProductForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('0', 'Varon'),
        ('1', 'Mujer'),
    )
    is_charger = ChoiceField(label='Cargador', widget=RadioSelect(attrs={'class':'form-group'}), choices=GENDER_CHOICES)

    class Meta:
        model = Product
        fields = ['name', 'description', 'product_brand', 'product_model', 'measures', 'color', 'is_charger', 'is_state']
        labels = {
            'name': 'Nombre Producto',
            'description': 'Descripcion Producto',
            'product_brand': 'Marca Producto',
            'product_model': 'Modelo Producto',
            'measures': 'Medidas',
            'color': 'Color',
            'is_charger': 'Cargador',
            'is_state': 'Estado'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre producto',
                    'id': 'name',
                    'name': 'name',
                    'required': 'required'
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripcion producto',
                    'id': 'description',
                    'name': 'description'
                }
            ),
            'product_brand': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Marca producto',
                    'id': 'product_brand',
                    'name': 'product_brand'
                }
            ),
            'product_model': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Modelo producto',
                    'id': 'product_model',
                    'name': 'product_model'
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Color producto',
                    'id': 'color',
                    'name': 'color'
                }
            ),
            'measures': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Medidas producto',
                    'id': 'measures',
                    'name': 'measures'
                }
            ),
            # 'is_charger': forms.RadioSelect(
            #     attrs={
            #         'class': 'form-check',
            #         'id': 'is_charger',
            #         'name': 'is_charger',
            #         'type': 'radio'
            #
            #     }
            # ),
            'is_state': forms.CheckboxInput(
                attrs={
                    'id': 'is_state',
                    'name': 'is_state'
                }
            )

        }
