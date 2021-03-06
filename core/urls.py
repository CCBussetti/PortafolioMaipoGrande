from django.urls import path , include
from .views import *
from rest_framework import routers
from django.conf.urls import url

rourter = routers.DefaultRouter()
rourter.register('productos',ProductoViewSet)

urlpatterns = [

    path('', index, name="index"),
    path('list_subastas/', list_subastas, name = "list_subastas"),
    path('ingresar_subasta/', ingresar_subasta, name = "ingresar_subasta"),
    path('mod_subastas/<id>/', mod_subasta, name = "mod_subastas"),
    path('eliminar_subasta/<id>/', eliminar_subasta, name = "eliminar_subasta"),
    path('api/', include(rourter.urls)),
    path('productos/',productos ,name = "productos"),
    path('eliminar-producto/<id>',eliminar_producto,name="eliminar_producto" ),
    path('modificarProducto/<id>/', modificarProducto, name="modificarProducto"),
    path('eliminarProducto/<id>/', eliminarProducto, name= "eliminarProducto"),
    path('ClientesExternos/', ClientesExternos,name= "ClientesExternos"),
    path('ClientesInternos/', ClientesInternos, name= "ClientesInternos"),
    path('modificarClienteI/<id>/', modificarClienteI,name="modificarClienteI"),
    #url(r'^modificarClienteE/(?P<NIE>\d+)/$', modificarClienteE, name='modificarClienteE'),
    path('modificarClienteE/<id>/', modificarClienteE, name="modificarClienteE"),
    path('eliminarClienteE/<id>/', eliminarClienteE, name= "eliminarClienteE"),
    path('eliminarClienteI/<id>/', eliminarClienteI, name="eliminarClienteI"),
    path('listado-productores/', listado_productores, name="listado_productores"),
    path('nuevos-productores/', nuevos_productores, name="nuevos_productores"),
    path('modificar-productores/<id>/', modificar_productores, name="modificar_productores"),
    path('eliminar-productores/<id>/', eliminar_productores, name="eliminar_productores"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registroClienteEx/', registroClienteEx, name='registroClienteEx'),
    path('registroClienteI/', registroClienteIn, name='registroClienteI'),
    path('registroProductor/', registroProductor, name='registroProductor'),
    path('list_solicitud_ext/', list_solicitud_ext, name='list_solicitud_ext'),
    path('ingresar_solicitud_ext/', ingresar_solicitud_ext, name='ingresar_solicitud_ext'),
    path('registroTransportista/', registroTransportista, name='registroTransportista'),
    path('mainPage_Externos/', mainPage_Externos, name='mainPage_Externos'),
    path('mainPage_Internos/', mainPage_Internos, name='mainPage_Internos'),
    path('prod_sobrante_disponible/', prod_sobrante_disponible, name='prod_sobrante_disponible'),
    path('list_proceso_local/', list_proceso_local, name='list_proceso_local'),
    path('ingresar_proceso_local/', ingresar_proceso_local, name='ingresar_proceso_local'),
    path('ing_proceso_local/<id>/', ing_proceso_local, name='ing_proceso_local'),
    path('ingresar_pago_interno/', ingresar_pago_interno, name='ingresar_pago_interno'),
    path('eliminar_producto_sobrante/<id>/', eliminar_producto_sobrante, name='eliminar_producto_sobrante'),
    path('productor',ProductorList.as_view(), name='Productor_list'),
]