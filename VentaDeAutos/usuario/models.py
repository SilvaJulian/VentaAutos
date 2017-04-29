from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
import datetime
# Create your models here.
class Usuarios(models.Model):
    usuario=models.OneToOneField(settings.AUTH_USER_MODEL)
    direccion=models.CharField(max_length=25,blank=True, null=True)
    fecha_publicacion=models.DateTimeField('Fecha',blank=True, null=True)
    
    #validacion telefono
    #telefono_regex = RegexValidator(regex=r'^\d{7,12}$', message="El formato de telefono debe ser: '4629160' o '03414629160'. ")
    telefono =  models.CharField(max_length=12,blank=True, null=True)
    #validacion celular
    #celular_regex = RegexValidator(regex=r'^\d{9,12}$', message="El formato del celular debe ser: '153354287' o '3413354287'. ")
    celular = models.CharField(max_length=12,blank=True, null=True)

    avatar=models.ImageField(upload_to='avatar',blank=True, null=True)
    #ver la direccion de guardar imagenes avatar
   # Activation toke for email verification
    activation_key = models.CharField(max_length=40, blank=True)
    restablecer_key= models.CharField(max_length=40, blank=True)
    # Expiration date for activation token
    key_expires = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.usuario.username

    def __unicode__(self):
    	return self.usuario
    
    def __unicode__(self):
        return str(self.usuario)
