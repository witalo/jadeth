import decimal
from django.db import models
from django.db.models import Sum, F
from django.db.models.functions import Coalesce

from apps.users.models import User
from django.utils import timezone

now = timezone.now()


# Create your models here.
class Order(models.Model):
    TYPE_CHOICES = (
        ('V', 'VENTA'),
        ('C', 'COMPRA'),
        ('M', 'EMPEÑO'),
        ('R', 'ENTREGA'),
        ('E', 'ENTRADA'),
        ('S', 'SALIDA')
    )
    STATUS_CHOICES = (('C', 'COMPLETADO'), ('P', 'PENDIENTE'), ('A', 'ANULADO'))
    id = models.AutoField(primary_key=True)
    type = models.CharField('TIPO', max_length=1, choices=TYPE_CHOICES, default='V')
    number = models.IntegerField(verbose_name='CORRELATIVO', null=True, blank=True)
    status = models.CharField('ESTADO', max_length=1, choices=STATUS_CHOICES, default='P')
    init = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    current = models.DateField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey('clients.Client', verbose_name='CLIENTE',
                               on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.ForeignKey('providers.Provider', verbose_name='PROVEEDOR',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    subsidiary = models.ForeignKey('users.Subsidiary', on_delete=models.CASCADE, null=True, blank=True)
    relative = models.IntegerField(verbose_name='ORDER RELACIONAL', default=0)

    def total(self):
        total = Detail.objects.filter(order=self).aggregate(
            r=Coalesce(Sum(F('quantity') * F('price')), decimal.Decimal(0.00))).get('r')
        return round(total, 2)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        ordering = ['id']

    def __str__(self):
        return str(self.type) + "-" + str(self.number)


class Detail(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('sales.Order', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.DecimalField('Cantidad', max_digits=10, decimal_places=2, default=0)
    old_quantity = models.DecimalField('Cantidad Anterior', max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField('Precio', max_digits=10, decimal_places=2, default=0)

    def amount(self):
        amount = round(decimal.Decimal(self.quantity * self.price), 2)
        return amount

    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        ordering = ['id']

    def __str__(self):
        return str(self.id)
