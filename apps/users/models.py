import os
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    return os.path.join('avatar/', filename)


class User(AbstractUser):
    document = models.CharField('Numero Documento', max_length=15, null=True, blank=True)
    phone = models.CharField('Celular', max_length=15, null=True, blank=True)
    avatar = models.ImageField('Foto', upload_to=get_file_path, blank=True, null=True)
    subsidiary = models.ForeignKey('Subsidiary', on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']

    def __str__(self):
        return self.email


class Subsidiary(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    serial = models.CharField(max_length=4, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(max_length=45, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    business_name = models.CharField('Razón social', max_length=100, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    token = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiales'
