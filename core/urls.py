from django.urls import path , include
from .views import ProductoViewSet , base, productos, listado_productores, nuevos_productores, modificar_productores, eliminar_productores
from rest_framework import routers

rourter = routers.DefaultRouter()
rourter.register('productos',ProductoViewSet)

urlpatterns = [
    path('', base, name="base"),
    path('api/', include(rourter.urls)),
    path('productos/',productos ,name = "productos"),
    path('listado-productores/', listado_productores, name="listado_productores"),
    path('nuevos-productores/', nuevos_productores, name="nuevos_productores"),
    path('modificar-productores/<id>/', modificar_productores, name="modificar_productores"),
    path('eliminar-productores/<id>/', eliminar_productores, name="eliminar_productores"),




]