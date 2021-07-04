from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import OperationalError
from application.parsers.parser import parse_price, ExceptionParseFail
from datetime import date
from time import sleep
from application.models import Produs, Pret, Lista
from .daily_update import BaseLogging

class Command(BaseCommand):
	help = 'Start the process for updating prices of the products in the database'
	
	def handle(self, *args, **options):
		self.job()
	
	def ensure_connection(self):
		db_conn = None
		while not db_conn:
			try:
				connection.ensure_connection()
				db_conn = True
			except OperationalError:
				self.stdout.write('Database unavailable, waiting 1 second')
				sleep(1)
				
	def job(self):
		log_file = BaseLogging()
		self.ensure_connection()
		number_of_update = 0
		number_of_fail = 0

		try:
			liste = Lista.objects.all()
		except Exception as err:
			log_file.error(f'Failed to open database {str(err)}')
			raise RuntimeError('Failed to open database') from err
			
		for lista in liste:
			timeline = []
			lista_produse = lista.produse()
			for produs in lista_produse:
				for pret in produs.preturi():
					pret_curent_time = pret.data_creare
					if not pret_curent_time in timeline:
						if pret_curent_time == date.today():
							pass
						else:	
							timeline.append(pret_curent_time)
					
			for produs in lista_produse:
				if produs.pret_final() != None:
					if produs.pret_final().data_creare == date.today():
						log_file.info(f'Skip update "{produs.nume}" Price already updated today')
						self.stdout.write(f'[INFO] Skip update "{produs.nume}" Price already updated today')
						continue

				try:
					new_price = parse_price(produs.site, produs.url)

					if len(produs.preturi()) != len(timeline):
						current_timeline = [pret.data_creare for pret in produs.preturi()]
						for t in timeline:
							if not t in current_timeline:
								p = Pret.objects.create(produs=produs, valoare=-1)
								p.data_creare = t
								p.save()
										
					Pret.objects.create(produs=produs, valoare=new_price, data_creare=date.today()) 	
					number_of_update += 1
					log_file.info(f'Updated "{produs.nume}" Price from {produs.site}')
					self.stdout.write(f'[INFO] Updated "{produs.nume}" Price from {produs.site}')
				except ExceptionParseFail as e:
					number_of_fail += 1
					log_file.warning(e.message)
					self.stdout.write(self.style.WARNING(f'[WARNING] Failed to get request from site {produs.site}, url: {produs.url}'))
		
		number_of_products = len(Produs.objects.all())
		message = f'Number of product prices updated: {number_of_update} out of {number_of_products}'
		log_file.info(message)
		self.stdout.write(f'[INFO] {message}')

		if number_of_fail > 0:
			message = f'Number of products that failed to update: {number_of_fail} out of {number_of_products}'
			log_file.warning(message)
			self.stdout.write(self.style.WARNING(f'[WARNING] {message}'))
		