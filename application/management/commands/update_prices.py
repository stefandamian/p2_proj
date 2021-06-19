from django.core.management.base import BaseCommand, CommandError
from application.parsers.parser import parse_price, ExceptionParseFail
import logging
from datetime import date
from time import sleep
import pidfile
from application.models import Produs, Pret, Lista

PID_FILE = 'update_prices.pid'

class Command(BaseCommand):
	help = 'Start the process for updating prices of the products in the database'
	
	def add_arguments(self, parser):
		parser.add_argument(
			'--manual',
			action='store_true',
			help='Update the prices at the time the command is given',
      )
	
	def handle(self, *args, **options):
		logging.basicConfig(level=logging.INFO, format='%(asctime)s[%(levelname)s]: %(message)s', filename='update_prices.log')
		if options['manual']:
			self.job()
		else:
			try:
				with pidfile.PIDFile(PID_FILE):
					self.stdout.write('[INFO] Process started')					
					logging.info("Process started")
					self.job()
					start_time = date.today()
					while True:
						if abs((date.today() - start_time).days) > 0:
							start_time = date.today()
							self.stdout.write('[INFO] Start updating prices')
							logging.info("Start updating prices")
							self.job()
						else:
							sleep(30)
			except pidfile.AlreadyRunningError:
				self.stdout.write(self.style.WARNING('[WARNING] Already running'))
				logging.warning("Already running")
				
	def job(self):
		number_of_update = 0
		number_of_fail = 0
		for lista in Lista.objects.all():
			timeline = []
			lista_produse = lista.produse()
			for produs in lista_produse:
				for pret in produs.preturi():
					if not pret.data_creare in timeline:
						if pret.data_creare == date.today():
							continue
						timeline.append(pret.data_creare)
					
			for produs in lista_produse:
				if produs.pret_final() != None:
					if produs.pret_final().data_creare == date.today():
						logging.info('Skip update "%s" Price already updated today', produs.nume)
						self.stdout.write(f'[INFO] Skip update {produs.nume} Price already updated today')
						continue

				try:
					new_price = parse_price(produs.site, produs.url)
					if len(produs.preturi()) != len(timeline):
						current_timeline = [pret.data_creare for pret in produs.preturi()]
						for time in timeline:
							if not time in current_timeline:
								Pret.objects.create(produs=produs, valoare=-1, data_creare=time)
					Pret.objects.create(produs=produs, valoare=new_price, data_creare=date.today()) 	
					number_of_update += 1
					logging.info('Updated "%s" Price from %s', produs.nume, produs.site)
					self.stdout.write(f'[INFO] Updated "{produs.nume}" Price from {produs.site}')
				except ExceptionParseFail as e:
					number_of_fail += 1
					logging.warning(e.message)
					self.stdout.write(self.style.WARNING(f'[WARNING] Failed to get request from site {produs.site}, url: {produs.url}'))
		
		number_of_products = len(Produs.objects.all())
		message = f'Number of product prices updated: {number_of_update} out of {number_of_products}'
		logging.info(message)
		self.stdout.write(f'[INFO] {message}')

		if number_of_fail > 0:
			message = f'Number of products that failed to update: {number_of_fail} out of {number_of_products}'
			logging.warning(message)
			self.stdout.write(self.style.WARNING(f'[WARNING] {message}'))
		