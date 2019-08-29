from django.contrib import admin
from .models import *


class MasProductoAdmin(admin.TabularInline):
    model = AumentoProducto
    extra = 1


class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'categoria', 'ref', 'activo', 'visible', 'cantidad', 'ficha']
    list_filter = ['categoria']
    readonly_fields = ['cantidad']
    inlines = [MasProductoAdmin]
    search_field = ['nombre']


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria']
    list_filter = ['categoria']
    search_field = ['categoria']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoriaproducto, CategoriaAdmin)
