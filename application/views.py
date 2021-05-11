from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from application.parsers.search import search, ExceptionSearchNotValid
from application.parsers.parser import parse
import application.parsers.constants as ct
from .models import Produs, Pret, Lista

def produse_view(request):
# creare pagina principala
	context = {
		"title": "Produse",
		"liste": Lista.objects.all()	
	}
	return render(request, 'lista_produse.html', context)

def add_produs_view(request):
	#nonfunctional si posibil de sters
	if request.method == "POST":
		Produs.objects.create(nume='neactualizat',
									url=request.POST.get("url"))
		return HttpResponseRedirect('/')
	context = {
		'title': 'Adaugare produs'	
	}
	return render(request, 'adauga_produs.html', context)
	
def add_lista_view(request):
	if request.method == 'GET':
		d = []
		for site in ct.supported_sites:
			name = request.GET.get("name")
			try:
				list_of_links = search(name, site)[:3] # maxim primele 3 produse care apar
			except ExceptionSearchNotValid as e:
				print(e.message)
			else:				
				#parsare fiecare link gasit din cautare pentru prezentare
				d1 = [parse(site, link) for link in list_of_links]
				d += d1
			 
		context = {
		'title': 'Cautare produs',
		'produse': d,
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
		return HttpResponseRedirect('/')		
			
			
def show_produs_view(request, id):
	#nonfunctional
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
	#nonfunctional si posibil de sters
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
    print(produse)
    for index, produs in enumerate(produse, start=1):
    	dataset = {}
    	preturi = Pret.objects.filter(produs=produs)
    	if index == 1:
    		labels = [pret.data_creare for pret in preturi]
    		data['labels'] = labels
    	dataset['data'] = [pret.valoare for pret in preturi]
    	dataset['label'] = f'produs {index}'
    	dataset['color_index'] = index
    	data['datasets'].append(dataset)
    return JsonResponse(data)
