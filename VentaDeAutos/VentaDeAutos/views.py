# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from usuario.models import Usuarios
from autos.models import Auto,Attachment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.utils import timezone



def raiz(request):
	all_cars = Auto.objects.all().order_by('-fecha_publicacion')
	fotos=[]
	for borrar_auto in all_cars:
		if timezone.now()>(borrar_auto.fecha_publicacion+ datetime.timedelta(90)):
			borrar_auto.delete()
	for i in all_cars:
		fotos.append(Attachment.objects.filter(auto_id=i.id)[0])
	page=request.GET.get('page')
	
	paginator=Paginator(fotos,9)
	try:
		lista=paginator.page(page)
	except PageNotAnInteger:
		lista=paginator.page(1)
	except EmptyPage:
		lista=paginator.page(paginator.num.pages)
	if request.user.is_authenticated():
		id_perfil=request.user.id
		usuario_perfil=Usuarios.objects.get(usuario_id=id_perfil)
		avatar=usuario_perfil.avatar		
		return render(request,'base.html',{'avatar':avatar,'autos':all_cars,'fotos':fotos,'lista':lista})
	else:
		return render(request,'base.html',{'autos':all_cars,'fotos':fotos,'lista':lista})

