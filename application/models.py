from django.db import models

# Create your models here.

class Lista(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=255)
	def produse(self):
		produse = [produs for produs in Produs.objects.filter(lista=self)]
		return produse

class Produs(models.Model):
	lista = models.ForeignKey(Lista, on_delete=models.CASCADE)
	site = models.CharField(max_length=255)	
	data_creare = models.DateField(auto_now_add=True, null=True)
	nume = models.CharField(max_length=255, null=True)
	url = models.URLField(max_length=450)
	poza = models.URLField(max_length=450, null=True)
	
	def preturi(self):
		preturi = [pret for pret in Pret.objects.filter(produs=self)]
		return preturi if len(preturi) > 0 else None
	
	def are_preturi(self):
		return self.preturi() != None	
			
	def pret_initial(self):
		preturi = self.preturi()	
		return None if preturi == None else preturi[0]
			
	def pret_final(self):
		preturi = self.preturi()	
		return None if preturi == None else preturi[-1] 
	
	def __str__(self):
		return f"Produs({self.nume}, {self.data_creare}, {self.url})"
		
class Pret(models.Model):
	produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
	valoare = models.FloatField()
	data_creare = models.DateField(auto_now_add=True, null=True)
        
	def __str__(self):
		return f"Pret({self.produs.__str__()}, {self.valoare}, {self.data})"

