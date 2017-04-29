# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import redirect,render,get_object_or_404
from django.core.urlresolvers import reverse
from usuario.forms import RegistroUsuariosForm,EditarMailForm,EditarPasswordForm,DatosPersonalesForm,DatosPersonales1Form
from autos.forms import CrearAutosForm
from usuario.models import Usuarios
from autos.models import Auto
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMessage
import hashlib, datetime, random
from django.utils import timezone
import hashlib, datetime, random
# Create your views here.



def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuariosForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            usuario = cleaned_data['nombre_usuario']
            password = cleaned_data['password']
            email = cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            fecha_publicacion=datetime.datetime.today()
            user_model=User.objects.create_user(username=usuario, password=password)
            user_model.email = email
            user_model.is_active=False# No está activo hasta que active el vínculo de verificación
            user_model.save()
            user_profile = Usuarios()
            user_profile.usuario=user_model
            user_profile.activation_key=activation_key
            user_profile.key_expires=key_expires
            user_profile.fecha_publicacion=fecha_publicacion
            user_profile.save()
            # Enviar un email de confirmación
            email_subject = 'Confirmacion de cuenta'
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da click en este link en menos de 48 horas: http://127.0.0.1:8000/cuenta/confirmacion/%s" % (usuario, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                [email], fail_silently=False)
            return redirect(reverse('cuenta.gracias', kwargs={'usuario':usuario}))
    else:
        form = RegistroUsuariosForm()
    return render(request, 'registro.html', {'form':form})

def confirmar_registro(request, activation_key):
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated():
        HttpResponseRedirect('base.html')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(Usuarios, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        return render_to_response('cuenta/confirmacion_caduco.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.usuario
    user.is_active = True
    user.save()
    usuario=user.username
    return redirect (reverse('cuenta.index', kwargs={'usuario':usuario}))

def gracias_view(request, usuario):
    messages.success(request,"%s gracias por registrarte. Le hemos mandado un email con un link para activar su cuenta. Saludos."%(usuario.capitalize()))
    return render(request,'gracias.html',{'usuario':usuario})

@login_required
def index_view(request,usuario):
    id_perfil=request.user.id
    editar=get_object_or_404(Usuarios,usuario_id=id_perfil)
    editar1=get_object_or_404(User,id=id_perfil)
    avatar=editar.avatar
    if request.method=='POST':
        ##Para guardar los datos del perfil es necesario agregar instance=request.user abajo!
        form=DatosPersonalesForm(request.POST, request.FILES,instance=editar)
        form1=DatosPersonales1Form(request.POST,instance=editar1)
        if form.is_valid() and form1.is_valid():
            form1.save()
            form.save()
            return redirect (reverse('cuenta.index', kwargs={'usuario':usuario}))
    else:
        form=DatosPersonalesForm(instance=editar)
        form1=DatosPersonales1Form(instance=editar1)
    return render(request,'index.html',{'form':form,'form1':form1,'avatar':avatar})

def login_view(request):

    if request.user.is_authenticated():
        return redirect (reverse('cuenta.index', kwargs={'usuario':usuario}))
    if request.method == 'POST':
        usuario= request.POST.get('usuario')
        password= request.POST.get('password')
        if '@' in usuario:
            usuario=User.objects.get(email=usuario).username
            user=authenticate(username=usuario,password=password)
        else:
            user=authenticate(username=usuario , password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect(reverse('cuenta.index', kwargs={'usuario':usuario}))
            else:
                messages.info(request, 'Su cuenta todavia no ha sido activada, verifique su email para confirmar cuenta.')
        messages.error(request, 'Nombre de usuario/email o contraseña no valido.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado')
    return redirect(reverse('cuenta.login'))

def recuperar_password(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email):
            user=User.objects.get(email=email)
            usuario=user.username
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            restablecer_key = hashlib.sha1(salt+email).hexdigest()
            usuario_key=Usuarios.objects.get(usuario_id=user.id)
            usuario_key.restablecer_key=restablecer_key
            usuario_key.save() 
            email_subject = u'Restrablecer contraseña'
            email_body = u"Hola %s, aqui le dejamos la contraseña para restablecer su cuenta. Para activar tu cuenta da click en este link en menos de 48 horas: http://127.0.0.1:8000/cuenta/restablecer_password/%s" % (usuario, restablecer_key)
            send_mail(email_subject, email_body, 'myemail@example.com',[email], fail_silently=False)
            messages.success(request,'El link para restablecer su contraseña ha sido enviado a su email.')
        else:
            messages.error(request,'Su email no esta registrado.')
    return render(request,'recuperar_contraseña.html')

def restablecer_password(request, restablecer_key):
    usuario_profile=get_object_or_404(Usuarios, restablecer_key=restablecer_key)
    user_profile=User.objects.get(id=usuario_profile.usuario_id)
    if request.method == 'POST':
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        if password==password2:
            user_profile.password=make_password(password)
            user_profile.save()
            usuario_profile.restablecer_key=''
            return redirect(reverse('cuenta.login'))
        else:
            messages.error(request,'Las contraseñas no coinciden')           
    return render(request,'restablecer_contraseña.html')

@login_required
def editar_mail(request,usuario):
    id_perfil=request.user.id
    avatar=get_object_or_404(Usuarios,usuario_id=id_perfil)
    avatar=avatar.avatar
    if request.method=='POST':
        form=EditarMailForm(request.POST,request=request)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            request.user.email=cleaned_data['email']
            request.user.save()
            messages.success(request,'El mail ha sido cambiado con exito')
            return redirect(reverse('cuenta.index',kwargs={'usuario':usuario}))
    else:
        form = EditarMailForm(request=request, initial={'email':request.user.email})
    return render(request, 'editar_mail.html', {'form': form,'avatar':avatar})

@login_required
def editar_password(request,usuario):
    id_perfil=request.user.id
    avatar=get_object_or_404(Usuarios,usuario_id=id_perfil)
    avatar=avatar.avatar
    errors=[]
    if request.method=='POST':
        form=EditarPasswordForm(request.POST)
        errors=[]
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['actual_password']):
                cleaned_data = form.cleaned_data
                password=cleaned_data['password']
                request.user.password=make_password(password)
                request.user.save()
                messages.success(request,'La contraseña ha sido cambiado con exito')
                messages.success(request, 'Es necesario introducir los datos para entrar.')            
                return redirect(reverse('cuenta.index',kwargs={'usuario':usuario}))
            else:
                errors.append('La contraseña no coincide con la actual')
    else:
        form=EditarPasswordForm()
    return render(request,'editar_contraseña.html',{'errors':errors, 'form':form,'avatar':avatar})

@login_required
def editar_mispublicaciones(request,usuario):

    id_perfil=request.user.id
    avatar=get_object_or_404(Usuarios,usuario_id=id_perfil)
    avatar=avatar.avatar
    autos=Auto.objects.all().filter(usuarios=usuario)
    return render(request,'editar_mis_publicaciones.html',{'autos':autos,'avatar':avatar})