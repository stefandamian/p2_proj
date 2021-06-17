from django.core.management.base import BaseCommand, CommandError
from subprocess import Popen
import os
import psutil

PID_FILE = 'get_prices.pid'
PY_FILE = 'get_prices.py'

def get_pid_from_file():
	if not os.path.exists(PID_FILE):
		return None		 
	with open(PID_FILE, "r") as f:
		try:
			pid = int(f.read())
		except (OSError, ValueError):
			return None
		return pid

def is_running():
	pid = get_pid_from_file()
	if pid == None:
		return False	
	try:
		os.kill(pid, 0)
	except OSError:
		return False
	else:
		return True

def kill_process():
	if is_running():
		os.kill(get_pid_from_file(), 1)
		os.system(f'sudo rm {PID_FILE}')

class Command(BaseCommand):
	help = 'Start the process for updating prices of the products in the database'
	
	def add_arguments(self, parser):
		parser.add_argument(
			'--stop',
			action='store_true',
			help='Stop the process',
      )
		parser.add_argument(
			'--manual',
			action='store_true',
			help='Update the prices at the time the command is given',
      )
	
	def handle(self, *args, **options):
		if options['stop']:
			kill_process()
		elif options['manual']:
			proc = Popen(['python', PY_FILE, '-m'])
			proc.wait()
		else:
			if not is_running():		
				pid = get_pid_from_file()
				if pid != None:
					os.system(f'sudo rm {PID_FILE}')
				proc = Popen(['python', PY_FILE])
		