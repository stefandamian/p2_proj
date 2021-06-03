from abc import ABC, abstractmethod
import urllib.request
from bs4 import BeautifulSoup
import time

class ExceptionParseFail(Exception):
	def __init__(self, url, message="The parsing has failed. site: X"):
		self.url = url
		self.message = message.replace('X', url)
		super().__init__(self.message)

class Parser(ABC):	
	@abstractmethod	
	def title(soup):
		pass
	@abstractmethod
	def photo(soup):
		pass
	@abstractmethod
	def price(soup):
		pass
		
	def __init__(self, site, url):
		self.site = site
		self.url = url
		
	def get_url(self):
		return self.url		
		
	def parse(self):
		request_done = False
		no_time = 0
		while((not request_done) and (no_time < 2)):
			try:
				web = urllib.request.urlopen(self.get_url())
				request_done = True
			except:
				time.sleep(1)
				no_time = no_time + 1
				print('failed to get request, will try again, url- '+ self.get_url())
		if not request_done:
			raise Exception(f'error: {self.get_url()} could not be resolved')
		if web.getcode() != 200:
			raise Exception(f'error: {web.getcode()}')
		
		soup = BeautifulSoup(web.read(), 'html.parser')
		return {
            'title': self.title(soup),
            'photo': self.photo(soup),
            'price': self.price(soup),
            'url': self.get_url(),
            'site': self.site
        }
	def parse_price(self):
		request_done = False
		no_time = 0
		while((not request_done) and (no_time < 2)):
			try:
				web = urllib.request.urlopen(self.get_url())
				request_done = True
			except:
				time.sleep(1)
				no_time = no_time + 1
				print('failed to get request, will try again, url- '+ self.get_url())
		if not request_done:
			raise Exception(f'error: {self.get_url()} could not be resolved')
		if web.getcode() != 200:
			raise Exception(f'error: {web.getcode()}')
		
		soup = BeautifulSoup(web.read(), 'html.parser')
		return self.price(soup)
		
class emag_parser(Parser):
	def title(self, soup):	
		result = soup.find('h1', {'class':'page-title'})
		if result != None:
			return result.contents[0].replace('\n', '').strip()
		raise ExceptionParseFail(self.url)
	def photo(self, soup):
		result = soup.find('img')
		if result != None:
			return result['src']
		raise ExceptionParseFail(self.url)
	def price(self, soup):
		result = soup.find('p', {'class':'product-new-price'})
		if result != None:
			p = result.contents
			p1 = p[0].replace('\n', '').replace('.', '').strip()
			return float(f"{p1}.{p[1].contents[0]}")
		raise ExceptionParseFail(self.url)
			
class flanco_parser(Parser):
	def title(self, soup):	
		result = soup.find(id='product-title') 
		if result != None:
			return result.contents[0].strip()
		raise ExceptionParseFail(self.url)
	def photo(self, soup):
		result = soup.find('img', {'itemprop':'thumbnail'})
		if result != None:
			return result['src']
		raise ExceptionParseFail(self.url)
	def price(self, soup):
		result = soup.find('span', {'itemprop':'price'})
		if result != None:
			return result['content']
		raise ExceptionParseFail(self.url)
			
class cel_parser(Parser):
	def get_url(self):
		if not 'https://www.cel.ro' in self.url:
			return f'https://www.cel.ro{self.url}'
		return self.url
	def title(self, soup):	
		result = soup.find(id='product-name')
		if result != None:
			return result.contents[0].strip()
		raise ExceptionParseFail(self.url)
	def photo(self, soup):
		result = soup.find(id='main-product-image')
		if result != None:
			return result['src']
		raise ExceptionParseFail(self.url)
	def price(self, soup):
		result = soup.find(id='product-price')
		if result != None:
			return result.contents[0]
		raise ExceptionParseFail(self.url)
		
distribute = {
    'emag': emag_parser,
    'flanco': flanco_parser,
    'cel': cel_parser
}
		
def parse(site, url):
    my_parser = distribute[site](site, url)
    return my_parser.parse()

def parse_price(site, url):
	my_parser = distribute[site](site, url)
	return my_parser.parse_price()