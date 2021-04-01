from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from .models import Produs, Pret

def produse_view(request):
	context = {
		"title": "Produse",
		"produse": Produs.objects.all()	
	}
	return render(request, 'lista_produse.html', context)

def add_produs_view(request):
	if request.method == "POST":
		Produs.objects.create(nume='neactualizat',
									url=request.POST.get("url"))
		return HttpResponseRedirect('/')
	context = {
		'title': 'Adaugare produs'	
	}
	return render(request, 'adauga_produs.html', context)
	
def show_produs_view(request, id):
	produs = Produs.objects.get(id=id)
	if request.method == "POST":
		if bool(request.POST.get("delete")):
			produs.delete()
		return HttpResponseRedirect('/')
	context = {
		'title': produs.nume,	
		'produs': produs
	}
	return render(request, 'vizualizare_produs.html', context)
	
def preturi_chart(request, id):
    produs = Produs.objects.get(id=id)
    preturi = Pret.objects.filter(produs=produs)
    return JsonResponse(data={
        'labels': [pret.data_creare for pret in preturi],
        'data': [pret.valoare for pret in preturi]
    })