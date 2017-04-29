# -*- coding: utf-8 -*-
from django.shortcuts import redirect,render,get_object_or_404
from django.core.urlresolvers import reverse
from autos.forms import CrearAutosForm
from usuario.forms import DatosPersonalesForm
from autos.models import Auto,Attachment
from usuario.models import Usuarios
#from multiupload.fields import MultiFileField
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages


# Create your views here.
@login_required
def cargar(request):
    id_perfil=request.user.id
    perfil=get_object_or_404(Usuarios,usuario_id=id_perfil)
    avatar=perfil.avatar
    editar=perfil
    if request.method == 'POST':
        form = CrearAutosForm(request.POST,request.FILES)
        form1=DatosPersonalesForm(request.POST,instance=editar)
        if form.is_valid() and form1.is_valid():
            form1.save()
            carga_auto = form.save(commit=False)
            carga_auto.usuarios=request.user.username
            carga_auto.fecha_publicacion=timezone.now()
            carga_auto.save()
            for each in form.cleaned_data['attachments']:
                Attachment.objects.create(file=each,auto_id=carga_auto.id)
            carga_auto.save()
            return redirect(reverse('auto.cargar'))
    else:
        form=CrearAutosForm()
        form1=DatosPersonalesForm(instance=editar)
    return render(request,'cargar.html',{'form':form,'form1':form1,'avatar':avatar,'usuario':perfil})


@login_required
def editar_publicacion(request,idauto,usuario):
    id_perfil=request.user.id
    avatar=get_object_or_404(Usuarios,usuario_id=id_perfil)
    avatar=avatar.avatar
    editar=get_object_or_404(Auto,id=idauto)
    fotos=Attachment.objects.filter(auto_id=idauto)
    if request.method=='POST':
        form=CrearAutosForm(request.POST,request.FILES, instance=editar)
        if form.is_valid():
            carga_auto = form.save(commit=False)
            carga_auto.usuarios=request.user.username
            carga_auto.save()
            for each in form.cleaned_data['attachments']:
                Attachment.objects.create(file=each,auto_id=carga_auto.id)
            carga_auto.save()
            return redirect(reverse('cuenta.editar_publicacion',kwargs={'usuario':usuario,'idauto':idauto}))
    else:
        form=CrearAutosForm(instance=editar)
    return render(request,'editar_publicacion.html',{'form':form,'fotos':fotos,'avatar':avatar})

#eliminar
@login_required
def editar_eliminar_auto(request,idauto,usuario):
    autos=Auto.objects.get(id=idauto)
    autos.delete()
    return redirect(reverse('cuenta.editar_mispublicaciones',kwargs={'usuario':usuario}))

@login_required
def editar_eliminar_foto(request,idfoto,usuario):
    foto_auto=Attachment.objects.get(id=idfoto)
    idauto=foto_auto.auto_id
    foto_auto.delete()
    return redirect(reverse('cuenta.editar_publicacion',kwargs={'usuario':usuario ,'idauto':idauto}))

def contacto(request):
    if request.method=='POST':
        enviar_email=True
        if not request.POST.get('nombre', ''):
            messages.error(request, 'Ingrese Nombre y Apellido.', extra_tags='nombre')
            enviar_email=False
        if not request.POST.get('asunto', ''):
            messages.error(request, 'Ingrese asunto.', extra_tags='asunto')
            enviar_email=False
        if not request.POST.get('telefono', ''):
            messages.error(request, 'Ingrese telefono.', extra_tags='telefono')
            enviar_email=False
        if request.POST.get('email')=='' or ('@' not in request.POST['email']):
            messages.error(request, 'Ingrese email valido.', extra_tags='email')
            enviar_email=False
        if not request.POST.get('mensaje', ''):
            messages.error(request, 'Ingrese su mensaje.', extra_tags='mensaje')
            enviar_email=False
        if enviar_email==True:
            email_subject = request.POST['asunto']
            email_body = u" Usuario: %s.\n Telefono: %s .\n Email: %s .\n Mensaje: %s" %(request.POST['nombre'],request.POST['telefono'],request.POST['email'],request.POST['mensaje'])
            email_email=request.POST['email']
            send_mail(email_subject, email_body, email_email,['rosacartazzo@gmail.com'], fail_silently=False)
            messages.success(request, 'Mensaje enviado. Muchisimas gracias.')
    return render(request,'contacto.html')

def resultado(request):
    model = Auto
    form = CrearAutosForm
    errors=[]
    fotos=[]
    if 'q'or 'w' or 'e' or 'r'in request.GET:
        errors=[]
        q = request.GET['q']
        w= request.GET['w']
        e= request.GET['e']
        r= request.GET['r']
        t= request.GET['t']

        if not q and not w and not e and not r and not t:
            errors.append('Por favor introduce un termino de busqueda.')
        elif len(w)>15:
            errors.append('Por favor introduce un termino de busqueda menor a 15 caracteres.')
        else:
            if request.user.is_authenticated():
                id_perfil=request.user.id
                usuario_perfil=Usuarios.objects.get(usuario_id=id_perfil)
                avatar=usuario_perfil.avatar
                if t=="":
                    autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ))
                    for i in autos:
                        fotos.append(Attachment.objects.filter(auto_id=i.id)[0])                    
                    return render(request, 'resultado.html', {'autos': autos, 'query': q,'avatar':avatar,'fotos':fotos})
                else:
                    if int(t)<=(50000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__lte=int(t)))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'avatar':avatar,'fotos':fotos})
                    elif int(t)<=(100000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__range=(50000,int(t))))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'avatar':avatar,'fotos':fotos})
                    elif int(t)<(200000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__range=(100000,int(t))))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'avatar':avatar,'fotos':fotos})
                    elif int(t)>=(200000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__gte=int(t)))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'avatar':avatar,'fotos':fotos}) 
            else:
                if t=="":
                    autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ))
                    for i in autos:
                        fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                    return render(request, 'resultado.html', {'autos': autos, 'query': q,'fotos':fotos})
                else:
                    if int(t)<=(50000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__lte=int(t)))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'fotos':fotos})
                    elif int(t)<=(100000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__range=(50000,int(t))))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'fotos':fotos})
                    elif int(t)<(200000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__range=(100000,int(t))))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'fotos':fotos})
                    elif int(t)>=(200000):
                        autos = Auto.objects.filter(Q(marca__icontains=q) , Q(version__icontains=w ), Q(fabricacion__icontains=e ), Q(combustible__icontains=r ),Q(precio__gte=int(t)))
                        for i in autos:
                            fotos.append(Attachment.objects.filter(auto_id=i.id)[0]) 
                        return render(request, 'resultado.html', {'autos': autos, 'query': q,'fotos':fotos}) 


    return render(request,'buscar.html',{'errors':errors, 'form':form})

def detalles(request,idauto):
    autos=Auto.objects.get(id=idauto)
    auto_usuario=Usuarios.objects.get(usuario=User.objects.get(username=autos.usuarios).id)
    fotos=Attachment.objects.filter(auto_id=idauto)
    foto_socialmedia=Attachment.objects.filter(auto_id=idauto)[0]
    usuario_perfil=User.objects.get(id=auto_usuario.usuario_id)
    if request.user.is_authenticated():
        avatar=auto_usuario.avatar
        context={'autos':autos,'auto_usuario':auto_usuario,'avatar':avatar,'usuario_perfil':usuario_perfil,'fotos':fotos,'foto_socialmedia':foto_socialmedia}
        return render(request,'detalles.html',context)
    else:
        context={'autos':autos,'auto_usuario':auto_usuario,'usuario_perfil':usuario_perfil,'fotos':fotos,'foto_socialmedia':foto_socialmedia}
        return render(request,'detalles.html',context)