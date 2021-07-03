from django.core.management.base import BaseCommand
import logging
from datetime import date
from time import sleep
import pidfile
from subprocess import Popen, PIPE

class BaseLogging():

	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		self.formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
		self.file_handler = logging.FileHandler('daily_update.log')
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)
        
	def info(self, msg, *args):
		if isinstance(msg, str):
			self.logger.info(msg, *args)
		else:
			raise TypeError("The parameter for logging.info should be string")
			
	def warning(self, msg, *args):
		if isinstance(msg, str):
			self.logger.warning(msg, *args)
		else:
			raise TypeError("The parameter for logging.warning should be string")
			
	def debug(self, msg, *args):
		if isinstance(msg, str):
			self.logger.debug(msg, *args)
		else:
			raise TypeError("The parameter for logging.debug should be string")
			
	def error(self, msg, *args):
		if isinstance(msg, str):
			self.logger.error(msg, *args)
		else:
			raise TypeError("The parameter for logging.error should be string")

PID_FILE = 'daily_update.pid'

class Command(BaseCommand):
	help = 'Daily start the update_prices process'
		
	def add_arguments(self, parser):
		parser.add_argument(
			'--manual',
			action='store_true',
			help='Update the prices at the time the command is given',
      )
	
	def handle(self, *args, **options):
		log_file = BaseLogging()	
		try:
			with pidfile.PIDFile(PID_FILE):
				self.stdout.write(f'[INFO] Process started {str(date.today())}')
				log_file.info(f'Process started {str(date.today())}')					
				start_time = date.today()
				while True:
					if abs((date.today() - start_time).days) > 0:
						start_time = date.today()
						log_file.info('Start update_prices')						
						proc = Popen("p2_runserver update_prices", stdin=PIPE, stdout=PIPE, stderr=PIPE)
						out, errs = proc.communicate()
						if proc.returncode != 0:
							log_file.error('Process "p2_runserver update_prices" could not be started')
						else:
							log_file.info('Process update_prices finished succesfully')					
					else:
						sleep(30)
		except pidfile.AlreadyRunningError:
			self.stdout.write(self.style.WARNING('[WARNING] Already running'))
			log_file.warning("Already running")
			