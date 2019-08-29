from django.urls import path
from .views import ProductoLista

app_name = 'producto'
urlpatterns = [
    path('', ProductoLista, name='productos'),
]