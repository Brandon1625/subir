from django.contrib import admin
from .models import *
from import_export import resources
from import_export import fields
from import_export.admin import ExportMixin


class ModeloResource(resources.ModelResource):
    class Meta:
        model = Vale
        fields = [
            'no_vale', 'comprador', 'fecha', 'total',
            'pago', 'vendedor'
        ]
        export_order = [
            'no_vale', 'comprador', 'fecha', 'total',
            'pago', 'vendedor'
        ]


class DetalleAdmin(admin.TabularInline):
    model = Detalle_Vale
    extra = 5
    readonly_fields = ['subtotal']


class ValeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = [
        'no_vale', 'vendedor', 'comprador',
        'fecha', 'pago', 'total', 'ficha']
    list_filter = ['vendedor', 'fecha']
    inlines = [DetalleAdmin]
    readonly_fields = ['total']
    exclude = ['no_vale']
    search_fields = ['comprador']

admin.site.register(Vale, ValeAdmin)
