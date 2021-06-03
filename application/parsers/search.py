import urllib.request
from bs4 import BeautifulSoup
from application.parsers.constants import *
import time

class ExceptionSearchNotValid(Exception):
	def __init__(self, search, site, message="error: \"X\" is not a valid search"):
		self.site = site		
		self.search = search
		self.message = message.replace('X', search)
		super().__init__(self.message)


def search(name, site):
	name = name.strip().lower()
	search_name = name.replace(' ', spacing[site])
	if len(name) == 0:
		return []
	url = f'{search_url[site]}{search_name}'
        
	print(url)
    
	request_done = False
	no_time = 0
	while((not request_done) and (no_time < 2)):
		try:
			web = urllib.request.urlopen(url)
			request_done = True
		except Exception as e:
			time.sleep(1)
			no_time = no_time + 1
			print('failed to get request, will try again, url- '+ url)
	if not request_done:
			raise Exception(f'error: {url} could not be resolved')
	if web.getcode() != 200:
		raise Exception(f'error: {web.getcode()}')
    
	soup = BeautifulSoup(web.read(), 'html.parser')
	
    
	if len(soup.find_all(*(validare[site]))) > 0:
		raise ExceptionSearchNotValid(name, site)   
        
	list_of_links = []
	result = soup.find(**(containter_produse[site]))
	if result != None:
	   for produs in result.find_all(*(containter_produs[site])):	
		   result = produs.find(*(link_produs[site]))
		   if result != None:
			   link = result['href']
			   list_of_links.append(link)
	
	return(list_of_links)