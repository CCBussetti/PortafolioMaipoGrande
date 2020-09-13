from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producto
        fields = ['nombre','precio', 'calidad','id_fruta','rut_productor']