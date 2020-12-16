# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser

class Adminc(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'adminc'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

#    REQUIRED_FIELDS = ['username']
#    USERNAME_FIELD = 'username'

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ClienteExterno(models.Model):
    nie = models.BigIntegerField(primary_key=True)
    nombre_cliex = models.CharField(max_length=25)
    apellido_cliex = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    id_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='id_pais')
    #user = models.CharField(max_length=255, blank=True, null=True)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    #user = models.OneToOneField('AuthUser', models.DO_NOTHING, db_column='username')
    #REQUIRED_FIELDS = ['user']
    #USERNAME_FIELD = 'nie'

    class Meta:
        managed = False
        db_table = 'cliente_externo'

    def __str__(self):
        return '%s %s' % ( self.nombre_cliex , self.apellido_cliex)


class ClienteInterno(models.Model):
    rut_clii = models.CharField(primary_key=True, max_length=10)
    nombre_clii = models.CharField(max_length=25)
    apellido_clii = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    id_comuna = models.ForeignKey('ComunaLocal', models.DO_NOTHING, db_column='id_comuna')
    #user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente_interno'

    def __str__(self):
        return self.rut_clii


class ComunaLocal(models.Model):
    id_comuna = models.BigAutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=150)
    id_region = models.ForeignKey('RegionLocal', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna_local'

    def __str__(self):
        return self.nombre_comuna


class Contrato(models.Model):
    id_contrato = models.BigAutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    rut_productor = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_productor')

    class Meta:
        managed = False
        db_table = 'contrato'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Estado(models.Model):
    id_estado = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'

    def __str__(self):
        return self.tipo
<<<<<<< HEAD

=======
>>>>>>> cristobal

class Fruta(models.Model):
    id_fruta = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'fruta'

    def __str__(self):
        return self.nombre


class MetodoPagoE(models.Model):
    id_metodo_pago = models.BigAutoField(primary_key=True)
    nombre_metodo_pago = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'metodo_pago_e'

    def __str__(self):
        return self.nombre_metodo_pago


class MetodoPagoL(models.Model):
    id_metodo_pago = models.BigAutoField(primary_key=True)
    nombre_metodo_pago = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'metodo_pago_l'

    def __str__(self):
        return self.nombre_metodo_pago


class PagoEx(models.Model):
    id_pagoex = models.BigAutoField(primary_key=True)
    fecha_pagoex = models.DateField(blank=True, null=True)
    id_metodo_pago = models.ForeignKey(MetodoPagoE, models.DO_NOTHING, db_column='id_metodo_pago')
    id_proceso_ex = models.ForeignKey('ProcesoVentaEx', models.DO_NOTHING, db_column='id_proceso_ex')

    class Meta:
        managed = False
        db_table = 'pago_ex'


class PagoI(models.Model):
    id_pagoi = models.BigAutoField(primary_key=True)
    fecha_pago = models.DateField()
    id_metodo_pago = models.ForeignKey(MetodoPagoL, models.DO_NOTHING, db_column='id_metodo_pago')
    id_vental = models.ForeignKey('ProcesoVentaLocal', models.DO_NOTHING, db_column='id_vental')

    class Meta:
        managed = False
        db_table = 'pago_i'


class Pais(models.Model):
    id_pais = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'pais'

    def __str__(self):
        return self.nombre


class ProcesoVentaEx(models.Model):
    id_proceso_ex = models.BigAutoField(primary_key=True)
    impuesto_aduana = models.BigIntegerField()
    comision_empresa = models.BigIntegerField()
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto')
    id_subasta = models.ForeignKey('Subasta', models.DO_NOTHING, db_column='id_subasta')
    id_solicitud = models.ForeignKey('SolicitudCompraExt', models.DO_NOTHING, db_column='id_solicitud')
    id_transf = models.ForeignKey('TransporteFinal', models.DO_NOTHING, db_column='id_transf')

    class Meta:
        managed = False
        db_table = 'proceso_venta_ex'


class ProcesoVentaLocal(models.Model):
    id_vental = models.BigAutoField(primary_key=True)
    costo_transporte = models.BigIntegerField()
    comision_empresa = models.BigIntegerField(blank=True, null=True)
    rut_clii = models.ForeignKey(ClienteInterno, models.DO_NOTHING, db_column='rut_clii')
    id_produs = models.ForeignKey('ProductoSobrante', models.DO_NOTHING, db_column='id_produs')
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')

    class Meta:
        managed = False
        db_table = 'proceso_venta_local'


class Producto(models.Model):
    id_producto = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=25)
    precio = models.BigIntegerField()
    calidad = models.BigIntegerField()
    id_fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='id_fruta')
    rut_productor = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_productor')

    class Meta:
        managed = False
        db_table = 'producto'

    def __str__(self):
        return self.nombre


class ProductoSobrante(models.Model):
    id_produs = models.BigAutoField(primary_key=True)
    precio_kilo = models.BigIntegerField()
    stock = models.BigIntegerField()
    id_fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='id_fruta')
    rut_productor = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_productor')

    class Meta:
        managed = False
        db_table = 'producto_sobrante'



class Productor(models.Model):
    rut_productor = models.CharField(primary_key=True, max_length=10)
    nombre_productor = models.CharField(max_length=25)
    apellido_productor = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    #user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productor'

    def __str__(self):
        return '%s %s' % (self.nombre_productor , self.apellido_productor)

class RegionLocal(models.Model):
    id_region = models.BigAutoField(primary_key=True)
    nombre_region = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'region_local'

    def __str__(self):
        return self.nombre_region


class ReporteEx(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    id_pagoe = models.BigIntegerField()
    id_pagoex = models.ForeignKey(PagoEx, models.DO_NOTHING, db_column='id_pagoex')

    class Meta:
        managed = False
        db_table = 'reporte_ex'


class ReporteLocal(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    id_pagoi = models.ForeignKey(PagoI, models.DO_NOTHING, db_column='id_pagoi')

    class Meta:
        managed = False
        db_table = 'reporte_local'


class SolicitudCompraExt(models.Model):
    id_solicitud = models.BigAutoField(primary_key=True)
    presupuesto = models.BigIntegerField()
    id_producto = models.BigIntegerField(verbose_name="Cantidad(Kg)")
    nie = models.ForeignKey(ClienteExterno, models.DO_NOTHING, db_column='nie', verbose_name="Cliente")
    id_fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='id_fruta',verbose_name="Tipo de Fruta")
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')

    class Meta:
        managed = False
        db_table = 'solicitud_compra_ext'

   
    


class Subasta(models.Model):
    id_subasta = models.BigAutoField(primary_key=True)
    costo_transporte = models.BigIntegerField()
    rut_transportista = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='rut_transportista')

    class Meta:
        managed = False
        db_table = 'subasta'


class TransporteFinal(models.Model):
    id_transf = models.BigAutoField(primary_key=True)
    seguro = models.CharField(max_length=2)
    coste_seguro = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'transporte_final'


class Transportista(models.Model):
    rut_transportista = models.CharField(primary_key=True, max_length=10)
    nombre_transportista = models.CharField(max_length=25)
    apellido_transportista = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    #user = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transportista'
    
    def __str__(self):
        return '%s %s' % (self.nombre_transportista , self.apellido_transportista)

    def __str__(self):
        return self.rut_transportista


class Vehiculo(models.Model):
    patente = models.CharField(primary_key=True, max_length=6)
    capacidad = models.BigIntegerField()
    refigeracion = models.CharField(max_length=2)
    tamanio = models.CharField(max_length=25)
    rut_transportista = models.ForeignKey(Transportista, models.DO_NOTHING, db_column='rut_transportista')

    class Meta:
        managed = False
        db_table = 'vehiculo'

    def __str__(self):
        return self.patente
