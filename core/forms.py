from django import forms
from django.forms import ModelForm
from .models import *

class ProductorForm(ModelForm):

    class Meta:
        model = Productor
        fields = ['rut_productor', 'nombre_productor', 'apellido_productor', 'telefono', 'email']