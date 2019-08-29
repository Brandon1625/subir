from django.contrib import admin
from .models import *


class TrabajadorAdmin(admin.ModelAdmin):

    readonly_fields = ['codigo']
    list_display = [
     'codigo', 'nombre', 'apellido', 'direccion', 'telefono',
     'fecha_nacimiento', 'ficha'
     ]
    list_filter = ['direccion', 'apellido']
    search_fields = ['nombre']

admin.site.register(Trabajador, TrabajadorAdmin)
