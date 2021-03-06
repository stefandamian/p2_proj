from django.contrib import admin
from .models import *

class ProduseInline(admin.StackedInline):
    model = Produs
    extra = 1
    
class PretInline(admin.StackedInline):
    model = Pret
    extra = 1

class ListaAdmin(admin.ModelAdmin):
	list_display = ('name', 'user')
	fields = ('name', 'user')
	inlines = [ProduseInline]
	

class ProdusAdmin(admin.ModelAdmin):
	list_display = ('nume', 'lista', 'site', 'data_creare')
	fields = ('lista', ('site', 'nume', 'url'))
	inlines = [PretInline]
	

class PretAdmin(admin.ModelAdmin):
	list_display = ('produs', 'valoare', 'data_creare')
	fields = ('produs', 'valoare')
	

	
admin.site.register(Lista, ListaAdmin)
admin.site.register(Produs, ProdusAdmin)	
admin.site.register(Pret, PretAdmin)