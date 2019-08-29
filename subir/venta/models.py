from django.db import models
from producto.models import Producto
from cliente.models import Cliente
from comun.models import Tipopago
from trabajador.models import Trabajador
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


class Vale(models.Model):
    no_vale = models.IntegerField('No de venta', null=True, blank=True)
    comprador = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField('Fecha emision')
    pago = models.ForeignKey(
        Tipopago, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE, null=True, blank=True)
    total = models.FloatField('Total', default=0.00, null=True, blank=True)

    def __str__(self):
        return "%s" % (self.no_vale)

    def clean(self):
        if not self.id:
            vale = Vale.objects.all().order_by('no_vale').last()
            self.no_vale = 100 if not vale else vale.no_vale+1

    def ficha(self):
        return mark_safe(u'<a href="/ProyectoFinal/ficha/?id=%s" target="_blank">Imprimir</a>' % self.id)
    ficha.short_description = 'Imprimir'

    class Meta:
        db_table = 'vale'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'


class Detalle_Vale(models.Model):
    id_vale = models.ForeignKey(
        Vale, on_delete=models.CASCADE, null=True,
        blank=True, related_name='detalles')
    id_prod = models.ForeignKey(
        Producto, on_delete=models.CASCADE, null=True, blank=True)
    canti = models.FloatField('Cantidad', default=0)
    precio = models.FloatField('Precio')
    subtotal = models.FloatField('Subtotal', null=True, blank=True, editable=False)

    def clean(self):
        self.subtotal = self.canti * self.precio
        if self.id:
            actual = Detalle_Vale.objects.filter(id=self.id)[0]
            if self.canti <= self.id_prod.cantidad + actual.canti:
                self.id_prod.cantidad = self.id_prod.cantidad + actual.canti - self.canti
                self.id_prod.save()

            else:
                raise ValidationError('La cantidad es mayor a las existencias porque la existencia es {}'.format(self.id_prod.cantidad))
        elif self.canti <= self.id_prod.cantidad:
                self.id_prod.cantidad = self.id_prod.cantidad - self.canti
                self.id_prod.save()
        else:
            raise ValidationError('La cantidad es mayor a las existencias porque la existencia es {}'.format(self.id_prod.cantidad))

    def __str__(self):
        return "%s" % (self.id_vale)

    class Meta:
        db_table = 'detalle_vale'
        verbose_name = 'Detalle de venta'
        verbose_name_plural = 'Detalle de ventas'


@receiver(post_delete, sender=Detalle_Vale)
def trigger_borradodedetalle(sender, **kwargs):
    linea = kwargs.get('instance')
    vale = Vale.objects.get(id=linea.id_vale.id)
    producto = Producto.objects.get(id=linea.id_prod.id)
    vale.total = vale.detalles.aggregate(total=Sum(F('subtotal')))['total']
    producto.cantidad = producto.cantidad + linea.canti
    producto.save()
    vale.save()


# Trigger para guardar totales
@receiver(post_save, sender=Detalle_Vale)
def trigger_sumadevale(sender, **kwargs):
    linea = kwargs.get('instance')
    vale = Vale.objects.get(id=linea.id_vale.id)
    vale.total = vale.detalles.aggregate(total=Sum(F('subtotal')))['total']
    vale.save()
