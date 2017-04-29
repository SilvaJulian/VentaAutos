"""VentaDeAutos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
 #!/usr/bin/python
# encoding: utf-8-
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from VentaDeAutos.views import raiz
from autos.views import cargar,contacto,resultado,detalles,editar_publicacion,editar_eliminar_auto,editar_eliminar_foto
from usuario.views import registro_usuario,confirmar_registro,gracias_view,login_view,index_view,logout_view,recuperar_password,restablecer_password,editar_mail,editar_password,editar_mispublicaciones


urlpatterns = [
    url(r'^$', raiz,name='raiz'),
    url(r'^admin/',include(admin.site.urls)),
    url(r'^auto/cargar/$',cargar,name='auto.cargar'),
    url(r'^contacto/$', contacto, name='auto.contacto'),
    url(r'^auto/buscar/resultado/$', resultado, name='auto.resultado'),
    url(r'^auto/detalles/(?P<idauto>[0-9]+)/$',detalles , name='auto.detalles' ),
    url(r'^cuenta/registrar/$',registro_usuario,name='cuenta.registrar'),
    url(r'^cuenta/confirmacion/(?P<activation_key>\w+)/$',confirmar_registro, name='cuenta.confimar_registro'),
    url(r'^cuenta/(?P<usuario>[\w]+)/gracias/$', gracias_view, name='cuenta.gracias'),
    url(r'^cuenta/login/$', login_view, name='cuenta.login'),
    url(r'^cuenta/logout/$', logout_view,name='cuenta.logout'),
    url(r'^cuenta/recuperar_password/$', recuperar_password,name='cuenta.recuperar_password'),
    url(r'^cuenta/restablecer_password/(?P<restablecer_key>\w+)/$', restablecer_password,name='cuenta.restablecer_password'),
    url(r'^perfil/(?P<usuario>[\w]+)/$',index_view, name='cuenta.index'),
    url(r'^perfil/(?P<usuario>[\w]+)/editar_mail/$',editar_mail, name='cuenta.editar_mail'),
    url(r'^perfil/(?P<usuario>[\w]+)/editar_password/$',editar_password, name='cuenta.editar_password'),
    url(r'^perfil/(?P<usuario>[\w]+)/editar_publicaciones$',editar_mispublicaciones, name='cuenta.editar_mispublicaciones'),
    url(r'^perfil/(?P<usuario>[\w]+)/(?P<idauto>[0-9]+)/editar_publicacion/$',editar_publicacion, name='cuenta.editar_publicacion'),
    url(r'^perfil/(?P<usuario>[\w]+)/(?P<idauto>[0-9]+)/eliminar_auto/$',editar_eliminar_auto, name='cuenta.editar_eliminar_auto'),
    url(r'^perfil/(?P<usuario>[\w]+)/(?P<idfoto>[0-9]+)/eliminar_imagen/$',editar_eliminar_foto, name='cuenta.editar_eliminar_foto'),
    ]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
