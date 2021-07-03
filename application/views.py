from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from application.parsers.search import search, ExceptionSearchNotValid
from application.parsers.parser import parse
from application.parsers.constants import *
from .models import Produs, Pret, Lista
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def logout_view(request):
   logout(request)
   return redirect('/')
   
def user_profile_view(request):
	context = {
		'number_of_lists': 0,
		'number_of_products': 0,
		'user': request.user	
	}
	
	liste = Lista.objects.filter(user=request.user)
	if len(liste) > 0:
		context['number_of_lists'] = len(liste)
		for l in liste:
			context['number_of_products'] += len(l.produse())
	
	return render(request, 'user_profile.html', context)
    
def register_view(request):
	context = {
		"error_message": None
		}
	if request.method == "POST":
		#username check
		username = request.POST.get("username")
		if len(User.objects.filter(username=username)) > 0:
			context["error_message"] = f"Name \"{username}\" already used. Please try a different username."
		if context["error_message"] != None:
			print(context["error_message"])
			return render(request, 'registration/register.html', context)
		
		#mail check
		email = request.POST.get("email")
		if len(User.objects.filter(email=email)) > 0:
			context["error_message"] = f"Email \"{email}\" already used."
		if context["error_message"] != None:
			print(context["error_message"])
			return render(request, 'registration/register.html', context)
		
		#password check	
		password = request.POST.get("password")
		confirm_password = request.POST.get("password")
		if password != confirm_password:
			context["error_message"] = "Passwords don't match"
		if context["error_message"] != None:
			print(context["error_message"])
			return render(request, 'registration/register.html', context)
		try:
			new_user = User.objects.create_user(username=username, email=email, password=password)
			new_user = authenticate(username=username, password=password)
			login(request, new_user)
			return redirect(reverse('home'))
		except Exception as e:
			print(e)
			error_message = str(e)
	
	return render(request, 'registration/register.html', context)
	
def reset_password_done_view(request):
	info_message = "Password reset completed."
	return redirect('/')	

@login_required
def home_view(request):
	context = {
		"title": "Home"	
	}
	return render(request, 'home.html', context)

@login_required
def produse_view(request):
	context = {
		"title": "Produse",
		"liste": Lista.objects.filter(user=request.user)	
	}
	return render(request, 'lista_produse.html', context)
	
@login_required
def add_lista_view(request):
	if request.method == 'GET':
		produse_gasite = []
		for site in supported_sites:
			name = request.GET.get("name")
			try:
				list_of_links = search(name, site)
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
		id_lista = Lista.objects.create(name=name, user=request.user)
		for produs in products:
			id_produs = Produs.objects.create(lista=id_lista, poza=produs['photo'], site=produs['site'], nume=produs['title'], url=produs['url'])
			Pret.objects.create(produs=id_produs, valoare=produs['price'])
		return HttpResponseRedirect('/produse/')		

@login_required
def show_lista_view(request, id):
	lista = Lista.objects.get(id=id)
	if lista.user != request.user:
		HttpResponseRedirect('/produse/')
	if request.method == "POST":
		if bool(request.POST.get("delete")):
			lista.delete()
		return HttpResponseRedirect('/produse/')
	context = {
		'title': lista.name,	
		'lista': lista
	}
	return render(request, 'vizualizare_lista.html', context)			
	
@login_required		
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
	
@login_required
def preturi_chart(request, id):
	#functional, dar nu se poate ajunge la cale "normal"
    produs = Produs.objects.get(id=id)
    preturi = Pret.objects.filter(produs=produs)
    return JsonResponse(data={
        'labels': [pret.data_creare for pret in preturi],
        'data': [pret.valoare for pret in preturi]
    })
    
@login_required
def preturi_lista_chart(request, id):
    lista = Lista.objects.get(id=id)
    produse = [p for p in Produs.objects.filter(lista=lista)]        	
    data = {
		'labels': [],
		'datasets': []    
    }
    for index, produs in enumerate(produse):
      dataset = {}
      preturi = Pret.objects.filter(produs=produs).order_by('data_creare')
      labels = [pret.data_creare for pret in preturi]    	
      if len(labels) > len(data['labels']):
        data['labels'] = labels
      dataset['data'] = [pret.valoare if pret.valoare > 0 else 'NaN' for pret in preturi]
      dataset['label'] = f'produs {index + 1}'
      dataset['color_index'] = index
      data['datasets'].append(dataset)
    return JsonResponse(data)
