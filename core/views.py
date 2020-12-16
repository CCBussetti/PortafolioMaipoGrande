from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from .models import *
from .forms import *
from .serializers import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import *
from django.db import connection
import cx_Oracle
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response




def index(request):
    return render(request,'core/index.html')


def Agregar_ClientesE(nie, nombre_cliex, apellido_cliex, telefono, email, id_pais):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_AGREGAR_CLIENTESE", [nie, nombre_cliex, apellido_cliex, telefono, email, id_pais, salida])
    return salida.getvalue()

def listadoClientesE():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CLIENTESE", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def listadoPais():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PAIS", [out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)
    
    return lista

def modificarClientesExternos(request, nie):
    data = {
        'ClientesExternos': listadoClientesE(),
        'pais': listadoPais(),
    }
    if request.method == 'POST':
        nie = request.POST.get('nie')
        nombre = request.POST.get('Nombre')
        apellido = request.POST.get('Apellido')
        email = request.POST.get('Email')
        telefono = request.POST.get('Telefono')
        id_pais = request.POST.get('Pais')
        salida = modificarClienteE(nie, nombre, apellido, telefono, email, id_pais)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            data['ClientesExternos'] = listadoClientesE()
        else:
            data['mensaje'] = 'No se ha podido modificar'
    
    return render(request, 'core/modificarClienteE.html', data) 

def modificarClienteE(nie, nombre_cliex, apellido_cliex, telefono, email, id_pais):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_ACTUALIZAR_CLIENTESE",[nie, nombre_cliex, apellido_cliex, telefono, email, id_pais, salida])
    return salida.getvalue()


@allowed_users(allowed_roles=['admin','Cliente_Externo_grupo'])
def eliminarClienteE(request, id):
    clienteE = ClienteExterno.objects.get(nie=id)
    clienteE.delete()
    
    return redirect(to= "ClientesExternos") 



@allowed_users(allowed_roles=['admin','Cliente_Externo_grupo'])
def ClientesExternos(request): #Agregar y listar
    clientesE = ClienteExterno.objects.all()
    data = {
        'form': ClienteExternoForm(),
        'ClientesE': clientesE
    }
    if request.method == 'POST':
        formulario = ClienteExternoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Guardado Correctamente'
    return render(request, 'core/ClientesExternos.html', data)


@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def eliminarClienteI(request,id):
    ClientesI = ClienteInterno.objects.get(rut_clii=id)
    ClientesI.delete()
    return redirect(to = 'ClientesInternos')

@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def modificarClienteI(request, id):
    ClientesI = ClienteInterno.objects.get(rut_clii=id)
    data = {
        'form': ClienteInternoForm(instance= ClientesI)
    }

    if request.method == 'POST':
        formulario= ClienteInternoForm(data=request.POST, instance= ClientesI)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado correctamente"
            data['form'] = formulario

    return render(request, 'core/modificarClienteI.html', data)


@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def ClientesInternos(request): #Agregar y listar
    ClientesI =ClienteInterno.objects.all()
    data = {
        'form': ClienteInternoForm(),
        'ClientesI': ClientesI
    }
    if request.method == 'POST':
        formulario = ClienteInternoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Guardado Correctamente'

    return render(request, 'core/ClientesInternos.html', data)

@permission_required('core.view_producto')
@allowed_users(allowed_roles=['admin','Productor_grupo'])

#@permission_required('core.view_producto')
def productos(request):
    data = {
        'productos':listado_productos,
        'tipo_fruta':listado_categorias_fruta,
        'id_productor':listado_idproductor_productos,
    }

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        id_fruta = request.POST.get('tipofruta')
        precio = request.POST.get('precio')
        calidad = request.POST.get('calidad')
        rut_productor = request.POST.get('id_productor')
        salida = agregar_producto(nombre,id_fruta,precio,calidad,rut_productor)
        if salida == 1:
            data['mensaje'] = 'Agregado Correctamente'
        else:
            data['mensaje'] = 'no se pudo agregar'
    
    if request.method == 'DELETE':
        id_producto = request.DELETE.get('id_producto')
        eliminar_producto(id_producto) 

    return render(request,'core/productos.html',data)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

#@permission_required('core.view_producto')

#@permission_required('core.view_producto')
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

#@permission_required('core.add_producto')

def agregar_producto(nombre,id_fruta,precio,calidad,rut_productor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc("SP_AGREGAR_PRODUCTO",[nombre,id_fruta,precio,calidad,rut_productor, salida])
    return salida.getvalue()

def eliminar_producto(id_producto):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc("SP_ELIMINAR_PRODUCTO",[id_producto])
    
def modificarProducto( request , id):
    producto = Producto.objects.get(id_producto=id)
    data = {
        'form': ProductoForm(instance=producto),
        'productos':listado_productos,
        'tipo_fruta':listado_categorias_fruta,
        'id_productor':listado_idproductor_productos,
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado Correctamente"
            data['form'] = formulario
    #return redirect(to = 'modificarProducto')
    return render(request, 'core/modificarProducto.html/', data)

def eliminarProducto(request,id):
    producto = Producto.objects.get(id_producto=id)
    producto.delete()
    return redirect(to = "productos")
    

@permission_required('core.view_subasta')
@allowed_users(allowed_roles=['admin','Transportista_grupo'])
def list_subastas(request):
    subasta = Subasta.objects.all()
    data_sub = {
        'subasta':subasta
    }
    return render(request,'core/list_subastas.html', data_sub)

@permission_required('core.add_subasta')
@allowed_users(allowed_roles=['admin','Transportista_grupo'])
def ingresar_subasta(request):
    data_sf = {
        'form':SubastaForm
    }
    if request.method == "POST":
        formulario = SubastaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data_sf['mensaje'] = "Subasta creada exitosamente"

    return render(request, 'core/ingresar_subasta.html', data_sf)

@permission_required('core.change_subasta')
@allowed_users(allowed_roles=['admin','Transportista_grupo'])
def mod_subasta(request, id):
    subasta = Subasta.objects.get(id_subasta=id)
    data_mod = {
        'form':SubastaForm(instance=subasta)
    }

    if request.method == 'POST':
        formulario = SubastaForm(data=request.POST, instance=subasta)
        if formulario.is_valid():
            formulario.save()
            data_mod['mensaje'] = "Subasta modificada exitosamente"
            data_mod['form'] = formulario

    return render(request, 'core/mod_subastas.html', data_mod)

@permission_required('core.delete_subasta')
@allowed_users(allowed_roles=['admin','Transportista_grupo'])
def eliminar_subasta(request, id):
    subasta = Subasta.objects.get(id_subasta=id)
    subasta.delete()
    return redirect(to="list_subastas")

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
        'form': ProductorForm(instance=productores),
        'productos':listado_productos,
        'tipo_fruta':listado_categorias_fruta,
        'id_productor':listado_idproductor_productos,
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

def registroClienteEx(request):
    if request.method == 'POST':
        form = RegistroClienteEx(request.POST)
        profile_form = ClienteExternoForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = profile_form.save()
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            g_clien_Ex, creado = Group.objects.get_or_create(name='Cliente_Externo_grupo')
            permiso1, c1 = Permission.objects.get_or_create(name='Can add estado')
            permiso2, c2 = Permission.objects.get_or_create(name='Can view estado')
            permiso3, c3 = Permission.objects.get_or_create(name='Can add fruta')
            permiso4, c4 = Permission.objects.get_or_create(name='Can change fruta')
            permiso5, c5 = Permission.objects.get_or_create(name='Can delete fruta')
            permiso6, c6 = Permission.objects.get_or_create(name='Can view fruta')
            permiso7, c7 = Permission.objects.get_or_create(name='Can add proceso venta ex')
            permiso8, c8 = Permission.objects.get_or_create(name='Can view proceso venta ex')
            permiso9, c9 = Permission.objects.get_or_create(name='Can add producto')
            permiso10, c10 = Permission.objects.get_or_create(name='Can view producto')
            permiso11, c11 = Permission.objects.get_or_create(name='Can add solicitud compra ext')
            permiso12, c12 = Permission.objects.get_or_create(name='Can view solicitud compra ext')
            permiso13, c13 = Permission.objects.get_or_create(name='Can change solicitud compra ext')
            permiso14, c14 = Permission.objects.get_or_create(name='Can delete solicitud compra ext')
            g_clien_Ex.permissions.add(permiso1, permiso2, permiso3, permiso4, permiso5, permiso6, permiso7, permiso8, permiso9, permiso10, permiso11, permiso12, permiso13, permiso14)
            user.groups.add(g_clien_Ex)
            login(request, user)
            return redirect('index')
    else:
        form = RegistroClienteEx()
        profile_form = ClienteExternoForm()
    return render(request, 'registration/registroClienteEx.html', {'form': form, 'profile_form': profile_form})

def registroClienteIn(request):
    if request.method == 'POST':
        form = RegistroClienteIn(request.POST)
        profile_form = ClienteInternoForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = profile_form.save()
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            g_clien_In, creado = Group.objects.get_or_create(name='Cliente_Interno_grupo')
            permiso1, c1 = Permission.objects.get_or_create(name='Can add fruta')
            permiso2, c2 = Permission.objects.get_or_create(name='Can change fruta')
            permiso3, c3 = Permission.objects.get_or_create(name='Can delete fruta')
            permiso4, c4 = Permission.objects.get_or_create(name='Can view fruta')
            permiso5, c5 = Permission.objects.get_or_create(name='Can add proceso venta local')
            permiso6, c6 = Permission.objects.get_or_create(name='Can change proceso venta local')
            permiso7, c7 = Permission.objects.get_or_create(name='Can delete proceso venta local')
            permiso8, c8 = Permission.objects.get_or_create(name='Can view proceso venta local')
            permiso9, c9 = Permission.objects.get_or_create(name='Can add producto sobrante')
            permiso10, c10 = Permission.objects.get_or_create(name='Can view producto sobrante')
            g_clien_In.permissions.add(permiso1, permiso2, permiso3, permiso4, permiso5, permiso6, permiso7, permiso8, permiso9, permiso10)
            user.groups.add(g_clien_In)
            login(request, user)
            return redirect('index')
    else:
        form = RegistroClienteIn()
        profile_form = ClienteInternoForm()
    return render(request, 'registration/registroClienteI.html', {'form': form, 'profile_form': profile_form})

def registroProductor(request):
    if request.method == 'POST':
        form = RegistroProductor(request.POST)
        profile_form = ProductorForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            g_prod, creado = Group.objects.get_or_create(name='Productor_grupo')
            permiso1, c1 = Permission.objects.get_or_create(name='Can add fruta')
            permiso2, c2 = Permission.objects.get_or_create(name='Can change fruta')
            permiso3, c3 = Permission.objects.get_or_create(name='Can delete fruta')
            permiso4, c4 = Permission.objects.get_or_create(name='Can view fruta')
            permiso5, c5 = Permission.objects.get_or_create(name='Can add producto')
            permiso6, c6 = Permission.objects.get_or_create(name='Can change producto')
            permiso7, c7 = Permission.objects.get_or_create(name='Can delete producto')
            permiso8, c8 = Permission.objects.get_or_create(name='Can view producto')
            permiso9, c9 = Permission.objects.get_or_create(name='Can add producto sobrante')
            permiso10, c10 = Permission.objects.get_or_create(name='Can change producto sobrante')
            permiso11, c11 = Permission.objects.get_or_create(name='Can delete producto sobrante')
            permiso12, c12 = Permission.objects.get_or_create(name='Can view producto sobrante')
            g_prod.permissions.add(permiso1, permiso2, permiso3, permiso4, permiso5, permiso6, permiso7, permiso8, permiso9, permiso10, permiso11, permiso12)
            user.groups.add(g_prod)
            login(request, user)
            return redirect('productos')
    else:
        form = RegistroProductor()
        profile_form = ProductorForm()
    return render(request, 'registration/registroProductor.html', {'form': form, 'profile_form': profile_form})

@allowed_users(allowed_roles=['admin'])
def registroTransportista(request):
    if request.method == 'POST':
        form = RegistroTransportista(request.POST)
        profile_form = TransportistaForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            g_transp, creado = Group.objects.get_or_create(name='Transportista_grupo')
            permiso1, c1 = Permission.objects.get_or_create(name='Can add subasta')
            permiso2, c2 = Permission.objects.get_or_create(name='Can change subasta')
            permiso3, c3 = Permission.objects.get_or_create(name='Can delete subasta')
            permiso4, c4 = Permission.objects.get_or_create(name='Can view subasta')
            permiso5, c5 = Permission.objects.get_or_create(name='Can view estado')
            permiso6, c6 = Permission.objects.get_or_create(name='Can add transporte final')
            permiso7, c7 = Permission.objects.get_or_create(name='Can change transporte final')
            permiso8, c8 = Permission.objects.get_or_create(name='Can delete transporte final')
            permiso9, c9 = Permission.objects.get_or_create(name='Can view transporte final')
            permiso10, c10 = Permission.objects.get_or_create(name='Can add vehiculo')
            permiso11, c11 = Permission.objects.get_or_create(name='Can change vehiculo')
            permiso12, c12 = Permission.objects.get_or_create(name='Can delete vehiculo')
            permiso13, c13 = Permission.objects.get_or_create(name='Can view vehiculo')
            g_transp.permissions.add(permiso1, permiso2, permiso3, permiso4, permiso5, permiso6, permiso7, permiso8, permiso9, permiso10, permiso11, permiso12, permiso13)
            user.groups.add(g_transp)
            login(request, user)
            return redirect('list_subastas')
    else:
        form = RegistroTransportista()
        profile_form = TransportistaForm()
    return render(request, 'registration/registroTransportista.html', {'form': form, 'profile_form': profile_form})

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Externo_grupo'])
def list_solicitud_ext(request):
    solicitud_ext = SolicitudCompraExt.objects.all()
    data = {'solicitud_ext': solicitud_ext}
    return render(request, 'core/list_solicitudes_ext.html', data)

@permission_required('core.add_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Externo_grupo'])
def ingresar_solicitud_ext(request):
    data = {
        'form': SolicitudExtForm()
    }
    if request.method == 'POST':
        formulario = SolicitudExtForm(request.POST)
        if formulario.is_valid() and SolicitudCompraExt:
            formulario.save()
            data['mensaje'] = "Solicitud guardada correctamente"

    return render(request, 'core/ingresar_solicitud_ext.html', data)

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Externo_grupo'])
def mainPage_Externos(request):
    return render(request, 'core/mainPage_Externos.html')

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def mainPage_Internos(request):
    return render(request, 'core/mainPage_Internos.html')

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def prod_sobrante_disponible(request):
    producto_sobrante = ProductoSobrante.objects.all()
    data = {'producto_sobrante': producto_sobrante}
    return render(request, 'core/prod_sobrante_disponible.html', data)

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def list_proceso_local(request):
    proceso_venta_local = ProcesoVentaLocal.objects.all()
    data = {'proceso_venta_local': proceso_venta_local}
    return render(request, 'core/list_proceso_local.html', data)

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def ingresar_proceso_local(request):
    data = {
        'form': ProcesoLocalForm()
    }

    if request.method == 'POST':
        formulario = ProcesoLocalForm(request.POST)
        if formulario.is_valid():
            formulario.save()
    return render(request, 'core/ingresar_proceso_local.html', data)

def ing_proceso_local(request, id):
    prod_sobrante = ProductoSobrante.objects.get(id_produs=id)
    prod_sobrante2 = ProcesoVentaLocal.objects.get(id_vental=id)
    if prod_sobrante == prod_sobrante2:
        data = {
        'form': ProcesoLocalForm(instance=prod_sobrante2)
        }
    elif prod_sobrante < prod_sobrante2:
        while prod_sobrante < prod_sobrante2:
            prod_sobrante2 = prod_sobrante2 + 1
        data = {
        'form': ProcesoLocalForm(instance=prod_sobrante2)
        }
    else:
        while prod_sobrante > prod_sobrante2:
            prod_sobrante2 = prod_sobrante2 - 1
        data = {
        'form': ProcesoLocalForm(instance=prod_sobrante2)
        }

    if request.method == 'POST':
        formulario = ProcesoLocalForm(data=request.POST, instance=prod_sobrante2)
        if formulario.is_valid():
            formulario.save()
            data['form'] = formulario
    return render(request, 'core/ing_proceso_local.html', data)

@permission_required('core.view_fruta')
@allowed_users(allowed_roles=['admin','Cliente_Interno_grupo'])
def ingresar_pago_interno(request):
    proceso_venta_local = ProcesoVentaLocal.objects.all()
    data = {
        'form': PagoInternoForm(),
        'proceso_venta_local': proceso_venta_local
    }
    if request.method == 'POST':
        formulario = PagoInternoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = 'Compra hecha con éxito, pulse el botón "Volver" para actualizar la compra'
    return render(request, 'core/ingresar_pago_interno.html', data)

def eliminar_producto_sobrante(request, id):
    producto_sobrante = ProductoSobrante.objects.get(id_produs=id)
    producto_sobrante.delete()

    return redirect(to='ingresar_pago_interno')

class ProductorList(generics.ListCreateAPIView):
    queryset = Productor.objects.all()
    serializer_class = ProductorSerializer
    permission_classes = {IsAuthenticated,}
    authentication_class = {TokenAuthentication,}

class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('core:Productor_list')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, *kwargs)
    
    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)

class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)

