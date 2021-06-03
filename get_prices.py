from application.parsers.parser import parse_price, ExceptionParseFail
import logging
from datetime import date
import schedule
import pidfile
import os
import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
  host="localhost",
  user="p2_user",
  password="qwer1234",
  database='ansamblu_automat_de_monitorizare'
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s[%(levelname)s]: %(message)s', filename='get_prices.log')

def job():
	mycursor = mydb.cursor()
	mycursor.execute("select id, site, url, nume from application_produs")
	produse = mycursor.fetchall()
	data_creare = str(date.today())
	for produs in produse:
		try:
			new_price = parse_price(produs[1], produs[2])
			mycursor.execute(f"INSERT INTO application_pret (valoare, produs_id, data_creare) Values ({new_price}, {produs[0]}, '{data_creare}')")
			mydb.commit()			
			logging.info('Updated "%s" Price from %s', produs[3], produs[2])
		except ExceptionParseFail as e:
			logging.warning(e.message)

logging.info("Starting process of get_prices")

try:
	with pidfile.PIDFile('get_prices.pid'):
		logging.info("Process started")
		schedule.every().day.at("02:00").do(job)

		while True:
			schedule.run_pending()
			sleep(30)
except pidfile.AlreadyRunningError:
	logging.warning("Already running")
    	
