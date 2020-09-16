# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ClienteExterno(models.Model):
    nie = models.BigIntegerField(primary_key=True)
    nombre_cliex = models.CharField(max_length=25)
    apellido_cliex = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    id_pais = models.ForeignKey('Pais', models.DO_NOTHING, db_column='id_pais')

    class Meta:
        managed = False
        db_table = 'cliente_externo'


class ClienteInterno(models.Model):
    rut_clii = models.CharField(primary_key=True, max_length=10)
    nombre_clii = models.CharField(max_length=25)
    apellido_clii = models.CharField(max_length=25)
    telefono = models.BigIntegerField()
    email = models.CharField(max_length=100)
    id_direccion = models.ForeignKey('DireccionLocal', models.DO_NOTHING, db_column='id_direccion')

    class Meta:
        managed = False
        db_table = 'cliente_interno'


class ComunaLocal(models.Model):
    id_comuna = models.BigAutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=150)
    id_region = models.ForeignKey('RegionLocal', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna_local'


class Contrato(models.Model):
    id_contrato = models.BigAutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    rut_productor = models.ForeignKey('Productor', models.DO_NOTHING, db_column='rut_productor')

    class Meta:
        managed = False
        db_table = 'contrato'


class DireccionLocal(models.Model):
    id_direccion = models.BigAutoField(primary_key=True)
    direccion = models.CharField(max_length=255)
    id_comuna = models.ForeignKey(ComunaLocal, models.DO_NOTHING, db_column='id_comuna')

    class Meta:
        managed = False
        db_table = 'direccion_local'


class Fruta(models.Model):
    id_fruta = models.FloatField(primary_key=True)
    nombre = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'fruta'


class MetodoPagoE(models.Model):
    id_metodo_pago = models.BigAutoField(primary_key=True)
    nombre_metodo_pago = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'metodo_pago_e'


class MetodoPagoL(models.Model):
    id_metodo_pago = models.BigAutoField(primary_key=True)
    nombre_metodo_pago = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'metodo_pago_l'


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

    class Meta:
        managed = False
        db_table = 'productor'


class RegionLocal(models.Model):
    id_region = models.BigAutoField(primary_key=True)
    nombre_region = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'region_local'


class ReporteEx(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=1000)
    id_pagoe = models.BigIntegerField()
    id_pagoex = models.ForeignKey(PagoEx, models.DO_NOTHING, db_column='id_pagoex')

    class Meta:
        managed = False
        db_table = 'reporte_ex'


class ReporteLocal(models.Model):
    id_reporte = models.BigAutoField(primary_key=True)
    descripcion = models.CharField(max_length=1000)
    id_pagoi = models.ForeignKey(PagoI, models.DO_NOTHING, db_column='id_pagoi')

    class Meta:
        managed = False
        db_table = 'reporte_local'


class SolicitudCompraExt(models.Model):
    id_solicitud = models.BigAutoField(primary_key=True)
    presupuesto = models.BigIntegerField()
    id_producto = models.BigIntegerField()
    nie = models.ForeignKey(ClienteExterno, models.DO_NOTHING, db_column='nie')
    id_fruta = models.ForeignKey(Fruta, models.DO_NOTHING, db_column='id_fruta')

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

    class Meta:
        managed = False
        db_table = 'transportista'


class Vehiculo(models.Model):
    patente = models.CharField(primary_key=True, max_length=6)
    capacidad = models.BigIntegerField()
    refigeracion = models.CharField(max_length=2)
    tamanio = models.CharField(max_length=25)
    rut_transportista = models.ForeignKey(Transportista, models.DO_NOTHING, db_column='rut_transportista')

    class Meta:
        managed = False
        db_table = 'vehiculo'
