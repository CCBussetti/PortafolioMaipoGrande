from django.urls import path , include
from .views import ProductoViewSet , home
from rest_framework import routers

rourter = routers.DefaultRouter()
rourter.register('productos',ProductoViewSet)

urlpatterns = [
    path('', home, name="home"),
    path('api/', include(rourter.urls)),
]