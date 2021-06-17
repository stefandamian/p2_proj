from application.parsers.parser import parse_price, ExceptionParseFail
import logging
from datetime import date, datetime
import time
import pidfile
import os
import mysql.connector
from time import sleep
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="p2_user",
  password="qwer1234",
  database='ansamblu_automat_de_monitorizare'
)

def job():
	mycursor = mydb.cursor()
	mycursor.execute("select id, site, url, nume from application_produs")
	produse = mycursor.fetchall()
	data_creare = str(date.today())
	number_of_update = 0
	number_of_fail = 0
	for produs in produse:
		testcursor = mydb.cursor()
		testcursor.execute(f"select id, data_creare, produs_id from application_pret where produs_id = {produs[0]}")
		try:		
			last_added_price = testcursor.fetchall()[-1]
		except IndexError:
			pass
		else:
			if data_creare == str(last_added_price[1]):
				logging.info('Skip update "%s" Price already updated today', produs[3])
				print(f'[INFO] Skip update {produs[3]} Price already updated today')
				continue

		try:
			new_price = parse_price(produs[1], produs[2])
			mycursor.execute(f"INSERT INTO application_pret (valoare, produs_id, data_creare) Values ({new_price}, {produs[0]}, '{data_creare}')")
			mydb.commit()
			number_of_update += 1
			logging.info('Updated "%s" Price from %s', produs[3], produs[2])
			print(f'[INFO] Updated "{produs[3]}" Price from {produs[1]}')
		except ExceptionParseFail as e:
			number_of_fail += 1
			logging.warning(e.message)

			print(f'[WARNING] Failed to get request from site {produs[1]}, url: {produs[2]}')
	message = f'Number of product prices updated: {number_of_update} out of {len(produse)}'
	logging.info(message)
	print(f'[INFO] {message}')

	if number_of_fail > 0:
		message = f'Number of products that failed to update: {number_of_fail} out of {len(produse)}'
		logging.warning(message)
		print(f'[WARNING] {message}')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format='%(asctime)s[%(levelname)s]: %(message)s', filename='get_prices.log')
	args = sys.argv[1:]
	if len(args) == 0:
		try:
			with pidfile.PIDFile('get_prices.pid'):
				logging.info("Process started")
				start_time = date.today()
				while True:
					if abs((date.today() - start_time).days) > 0:
						start_time = date.today()
						logging.info("Start updating prices")
						job()
					else:
						sleep(30)
		except pidfile.AlreadyRunningError:
			logging.warning("Already running")
	elif len(args) == 1:
		if args[0] in ['-m', '--manual']:
			try:
				with pidfile.PIDFile('get_prices_manual_run.pid'):
					logging.info("Process started")
					job()
			except pidfile.AlreadyRunningError:
				logging.warning("Already running")
		else:
			raise Exception('[ERROR] Wrong argument')
	else:
		raise Exception('[ERROR] Too many arguments')
    	
