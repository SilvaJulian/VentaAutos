from django.contrib import admin
from autos.models import Auto,Attachment

# Register your models here.
class AttachmentInLine(admin.StackedInline):
    model=Attachment

class AutoAdmin(admin.ModelAdmin):
    inlines=[AttachmentInLine,]
    list_display = ("marca","version","usuarios","fecha_publicacion" )
    list_filter = ("fecha_publicacion",)


admin.site.register(Auto,AutoAdmin)
