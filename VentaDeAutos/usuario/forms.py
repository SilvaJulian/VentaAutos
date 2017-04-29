# -*- coding: utf-8 -*-
from django import forms
from django.forms import Textarea
from django.contrib.auth.models import User
from usuario.models import Usuarios
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator



class RegistroUsuariosForm(forms.Form):
    nombre_usuario = forms.CharField(label='Usuario',min_length=5,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña:',min_length=5,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repetir Contraseña:',min_length=5,widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_usuario(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['nombre_usuario']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return nombre_usuario

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual en la base de datos.')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

class EditarMailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditarMailForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email= self.cleaned_data['email']
        actual_email= self.request.user.email
        username=self.request.user.username
        if email != actual_email:
            existe=User.objects.filter(email=email).exclude(username=username)
            if existe:
                raise forms.ValidationError('Ya existe un email igual en la base de datos')
        return email

class EditarPasswordForm(forms.Form):
    actual_password=forms.CharField(min_length=5,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=5,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(min_length=5,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   
    def clean_password2(self):
        password=self.cleaned_data['password']
        password2= self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

#    def clean_actual_password(self):
#        actual_password=self.cleaned_data.get('actual_password', None)
#        if self.user.check_password(actualpassword):
#            raise forms.ValidationError('ERROR LPM')
#        return actual_password

class EditarFotoForm(forms.Form):
    foto = forms.ImageField(required=False)

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model=Usuarios
        fields=['direccion','telefono','celular','avatar']
        exclude = ['usuario']

class DatosPersonales1Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name',]
        labels={ 'first_name':'Nombre','last_name':'Apellido'}