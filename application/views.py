from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from application.parsers.search import search, ExceptionSearchNotValid
from application.parsers.parser import parse
from application.parsers.constants import *
from .models import Produs, Pret, Lista

def home_view(request):
	context = {
		"title": "Home"	
	}
	return render(request, 'home.html', context)

def produse_view(request):
	context = {
		"title": "Produse",
		"liste": Lista.objects.all()	
	}
	return render(request, 'lista_produse.html', context)
	
def add_lista_view(request):
	if request.method == 'GET':
		produse_gasite = []
		for site in supported_sites:
			name = request.GET.get("name")
			try:
				list_of_links = search(name, site)[:3] # maxim primele 3 produse care apar
			except ExceptionSearchNotValid as e:
				print(e.message)
			else:				
				#parsare fiecare link gasit din cautare pentru prezentare
				produse_gasite_site = [parse(site, link) for link in list_of_links]
				produse_gasite += produse_gasite_site
			 
		context = {
		'title': 'Cautare produs',
		'produse': produse_gasite,
		'name': name	
		}
		return render(request, 'search_produs.html', context)
	elif request.method == 'POST':
		name = request.POST.get("name")
		checked = [tuple(element.split('|')) for element in request.POST.getlist("checked[]")]
		#reparsarea produselor selectate in crearea listei		
		products = [parse(*c) for c in checked]
		id_lista = Lista.objects.create(name=name)
		for produs in products:
			id_produs = Produs.objects.create(lista=id_lista, poza=produs['photo'], site=produs['site'], nume=produs['title'], url=produs['url'])
			Pret.objects.create(produs=id_produs, valoare=produs['price'])
		return HttpResponseRedirect('/produse/')		

def show_lista_view(request, id):
	lista = Lista.objects.get(id=id)
	if request.method == "POST":
		if bool(request.POST.get("delete")):
			lista.delete()
		return HttpResponseRedirect('/produse/')
	context = {
		'title': lista.name,	
		'lista': lista
	}
	return render(request, 'vizualizare_lista.html', context)			
			
def show_produs_view(request, id):
	#functional, dar nu se poate ajunge la cale "normal"
	produs = Produs.objects.get(id=id)
	if request.method == "POST":
		if bool(request.POST.get("delete")):
			produs.delete()
		return HttpResponseRedirect('/produse/')
	context = {
		'title': produs.nume,	
		'produs': produs
	}
	return render(request, 'vizualizare_produs.html', context)
	
def preturi_chart(request, id):
	#functional, dar nu se poate ajunge la cale "normal"
    produs = Produs.objects.get(id=id)
    preturi = Pret.objects.filter(produs=produs)
    return JsonResponse(data={
        'labels': [pret.data_creare for pret in preturi],
        'data': [pret.valoare for pret in preturi]
    })
    
def preturi_lista_chart(request, id):
    lista = Lista.objects.get(id=id)
    produse = [p for p in Produs.objects.filter(lista=lista)]        	
    data = {
		'labels': [],
		'datasets': []    
    }
    for index, produs in enumerate(produse):
      dataset = {}
      preturi = Pret.objects.filter(produs=produs)
      labels = [pret.data_creare for pret in preturi]    	
      if len(labels) > len(data['labels']):
        data['labels'] = labels
      dataset['data'] = [pret.valoare for pret in preturi]
      dataset['label'] = f'produs {index + 1}'
      dataset['color_index'] = index
      data['datasets'].append(dataset)
    return JsonResponse(data)
