from __future__ import unicode_literals
from decimal import Decimal
from django.db import models
from usuario.models import Usuarios
from django.utils.translation import ugettext_lazy as _
import datetime


# Create your models here.
class Auto(models.Model):
    marcas=(
        ('chevrolet','Chevrolet'),
        ('fiat','Fiat'),
        ('citroen','Citroen'),
        ('ford','Ford'),
        ('peugeot','Peugeot'),
        ('renault','Renault'),
        )
    combustibles=(
        ('nafta','Nafta'),
        ('gnc','Gnc'),
        ('diesel','Diesel'),
        )

    usuarios=models.CharField(max_length=18)
    marca = models.CharField(max_length=15,choices=marcas)
    version = models.CharField(max_length=20)
    kilometraje = models.IntegerField()
    combustible = models.CharField(max_length=10,choices=combustibles)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal(0))
    fabricacion=models.IntegerField()
    fecha_publicacion=models.DateTimeField('Fecha Publicacion',blank=True, null=True)
    def __unicode__(self):
        return self.marca

class Attachment(models.Model):
    auto = models.ForeignKey(Auto, verbose_name=_('Auto'))
    file = models.FileField(_('Imagenes'), upload_to='autos',blank=True, null=True)
    def __unicode__(self):
        return self.auto.marca
