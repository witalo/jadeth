from django.db import models
from django.forms import model_to_dict


# Create your models here.


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    document = models.CharField(max_length=15, blank=False, null=False, unique=True, default='')
    phone = models.CharField(max_length=9, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    is_state = models.BooleanField(default=True)

    def names(self):
        names = "{} {}".format(self.first_name, self.last_name)
        return names

    def to_json(self):
        dic = model_to_dict(self)
        return dic

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

    def __str__(self):
        return self.first_name
