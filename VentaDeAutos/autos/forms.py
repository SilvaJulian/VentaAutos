# -*- coding: utf-8 -*-
#importamos la api forms desde django
from django import forms
from multiupload.fields import MultiFileField
#Importamos los modelos
from autos.models import Auto,Attachment
from usuario.models import Usuarios

class CrearAutosForm(forms.ModelForm):
	class Meta:
		model = Auto
		fields=('marca','version','kilometraje','combustible','precio','fabricacion')
		exclude=['usuario']
	attachments = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)
	