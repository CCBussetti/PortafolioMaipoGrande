from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import *
from .forms import *
from .serializers import ProductoSerializer
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import connection
import cx_Oracle


# Create your views here.

@login_required
def base(request):
    return render(request,'core/base.html')

def productos(request):
    data = {
        'productos':listado_productos(),
        'tipo_fruta':listado_categorias_fruta(),
        'id_productor':listado_idproductor_productos(),
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        id_fruta = request.POST.get('tipofruta')
        precio = request.POST.get('precio')
        calidad = request.POST.get('calidad')
        rut_productor = request('id_productor')
        salida = agregar_producto(nombre,id_fruta,precio,calidad,rut_productor)
        if salida == 1:
            data['mensaje'] = 'Agregado Correctamente'
        else:
            data['mensaje'] = 'no se pudo agregar'

    return render(request,'core/productos.html',data)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset =Producto.objects.all()
    serializer_class = ProductoSerializer

## Procedimientos Almacenados
def listado_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_categorias_fruta():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPOFRUTA_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_idproductor_productos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_IDPRODUCTOR_PRODUCTOS", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def agregar_producto(nombre,id_fruta,precio,calidad,rut_productor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_AGREGAR_PRODUCTO",[nombre,id_fruta,precio,calidad,rut_productor, salida])
    return salida.getvalue()

def listado_productores(request):
    productores = Productor.objects.all()
    data = {
        'Productores': productores # la variable 'Peliculas ' definida en el diccionario python "data" es como debo llamar el listado de productores desde el template
    }
    return render(request, 'core/listado_productores.html', data)

def nuevos_productores(request):
    data = {
        'form': ProductorForm()
    }

    if request.method == "POST":
        formulario = ProductorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']="Guardado correctamente"

    return render(request, 'core/nuevos_productores.html', data)

def modificar_productores(request, id):
    productores = Productor.objects.get(rut_productor=id)
    data = {
        'form': ProductorForm(instance=productores)
    }

    if request.method == "POST":
        formulario = ProductorForm(data=request.POST, instance=productores)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado correctamente"
            data['form'] = formulario 
    return render(request, 'core/modificar_productores.html', data)

def eliminar_productores(request, id):
     productor = Productor.objects.get(rut_productor=id)
     productor.delete()

     return redirect(to="listado_productores")
    

