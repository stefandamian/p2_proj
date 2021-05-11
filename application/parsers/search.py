import urllib.request
from bs4 import BeautifulSoup
import application.parsers.constants as c
import time

class ExceptionSearchNotValid(Exception):
	def __init__(self, search, site, message="error: \"X\" is not a valid search"):
		self.site = site		
		self.search = search
		self.message = message.replace('X', search)
		super().__init__(self.message)


def search(name, site):
	name = name.strip()
	search_name = name.replace(' ', c.spacing[site])
    
	url = f'{c.search_url[site]}{search_name}'
        
	print(url)
    
	request_done = False
	no_time = 0
	while((not request_done) and (no_time < 2)):
		try:
			web = urllib.request.urlopen(url)
			request_done = True
		except:
			time.sleep(1)
			no_time = no_time + 1
			print('failed to get request, will try again, url- '+ url)
	if not request_done:
			raise Exception(f'error: {url} could not be resolved')
	if web.getcode() != 200:
		raise Exception(f'error: {web.getcode()}')
    
	soup = BeautifulSoup(web.read(), 'html.parser')
	
    
	if len(soup.find_all(*(c.validare[site]))) > 0:
		raise ExceptionSearchNotValid(name, site)   
        
	list_of_links = []
	for produs in soup.find(**(c.containter_produse[site])).find_all(*(c.containter_produs[site])):
		link = produs.find(*(c.link_produs[site]))['href']
		list_of_links.append(link)
	
	return(list_of_links)