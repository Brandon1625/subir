from django.contrib import admin
from .models import *
from django.shortcuts import redirect
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin


class ModeloResource(resources.ModelResource):
    class Meta:
        model = Cliente
        fields = [
            'nit', 'nombre', 'apellido', 'direccion',
            'email', 'activo'
        ]
        export_order = [
            'nit', 'nombre', 'apellido', 'direccion',
            'email', 'activo'
        ]


class ClienteAdmin(ExportMixin, admin.ModelAdmin):
    actions = ['inactivar', 'activar', 'informe']
    list_display = [
     'nit', 'nombre', 'apellido', 'direccion', 'email', 'activo', 'ficha'
     ]
    list_filter = ['direccion', 'activo']
    search_fields = ['nombre']

    def inactivar(self, request, queryset):

        for row in queryset.filter(activo=True):
            self.log_change(request, row, 'inactivar Cliente')
        rows_updated = 0

        for obj in queryset:
            if obj.activo:
                obj.activo = False
                obj.save()

                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 cliente se marco"
        else:
            message_bit = "%s clientes se marcaron" % rows_updated
        self.message_user(
            request, "%s satisfactoriamente como inactivos" % message_bit)
    inactivar.short_description = 'Inactivar cliente'

    def activar(self, request, queryset):
        for row in queryset.filter(activo=False):
            self.log_change(request, row, 'activar cliente')
        rows_updated = 0

        for obj in queryset:
            if not obj.activo:
                obj.activo = True
                obj.save()

                rows_updated += 1

        if rows_updated == 1:
            message_bit = "1 cliente se marco"
        else:
            message_bit = "%s clientes se marcaron" % rows_updated
        self.message_user(
            request, "%s satisfactoriamente como activos" % message_bit)
    activar.short_description = 'Activar Cliente'

    def informe(self, request, queryset):
        return redirect('/clientes')
    informe.short_description = 'Exportar clientes'

admin.site.register(Cliente, ClienteAdmin)
