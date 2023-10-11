import decimal

from django.db import models
import ast

# Create your models here.
from django.forms import model_to_dict


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=100, blank=True, null=True, default='-')
    product_brand = models.ForeignKey('products.ProductBrand', on_delete=models.CASCADE, default=None)
    product_model = models.ForeignKey('products.ProductModel', on_delete=models.CASCADE, default=None)
    measures = models.CharField(max_length=50, blank=True, null=True, default='-')
    color = models.CharField(max_length=300, blank=True, null=True, default=None)
    date_init = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    is_charger = models.BooleanField('Cargador', default=False)
    is_add = models.BooleanField('Adicional', default=False)
    is_state = models.BooleanField('Estado', default=True)

    def get_color(self):
        n = ast.literal_eval(self.color)
        color_set = Color.objects.filter(id__in=n)
        # print(color_set.values('name'))
        l = []
        for c in color_set:
            l.append(c.name)
        return l

    def get_store(self, u):
        store_set = Store.objects.filter(product=self, subsidiary__user=u)
        if store_set.exists():
            store_obj = store_set.first()
            return model_to_dict(store_obj)
        else:
            store = {'id': 0, 'product': self.name, 'subsidiary': 0, 'quantity': 0, 'price': 0}
            return store

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    product_brand = models.ForeignKey('ProductBrand', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['id']

    def __str__(self):
        return self.name


class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        ordering = ['id']

    def __str__(self):
        return self.name


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, default=None)
    subsidiary = models.ForeignKey('users.Subsidiary', on_delete=models.CASCADE, default=None)
    create_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, default=0)

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'
        ordering = ['id']
        unique_together = ('product', 'subsidiary')  # product y subsidiary unicos si los dos estan

    def __str__(self):
        return self.quantity
