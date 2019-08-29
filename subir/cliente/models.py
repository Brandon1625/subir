from django.db import models
from comun.models import Persona
from django.utils.safestring import mark_safe


class Cliente(Persona):
    nit = models.CharField('Nit', max_length=10, primary_key=True)
    email = models.EmailField('E-mail', max_length=50, null=True)
    activo = models.BooleanField(default=True, verbose_name='activo')

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    def ficha(self):
        return mark_safe(
            u'<a href="/clientesactivos"target="_blank">Imprimir</a>')
    ficha.short_description = 'Imprimir todos'

    class Meta:
        db_table = 'cliente'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
