from django.contrib import admin
from .models import *


class TipopagoAdmin(admin.ModelAdmin):
    search_fields = ['tipo']
    list_filter = ['tipo']
    list_display = ['tipo']

class ReferenciaAdmin(admin.ModelAdmin):
    search_fields = ['referencia']
    list_filter = ['referencia']
    list_display = ['referencia']

admin.site.register(Referencia, ReferenciaAdmin)
admin.site.register(Tipopago, TipopagoAdmin)
