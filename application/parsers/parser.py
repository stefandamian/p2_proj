from abc import ABC, abstractmethod
import urllib.request
from bs4 import BeautifulSoup
import time

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
		
class emag_parser(Parser):
	def title(self, soup):	
		return soup.find('h1', {'class':'page-title'}).contents[0].replace('\n', '').strip()
	def photo(self, soup):
		return soup.find('img')['src']
	def price(self, soup):
		p = soup.find('p', {'class':'product-new-price'}).contents
		p1 = p[0].replace('\n', '').replace('.', '').strip()
		return float(f"{p1}.{p[1].contents[0]}")
			
class flanco_parser(Parser):
	def title(self, soup):	
		return soup.find(id='product-title').contents[0].strip()
	def photo(self, soup):
		return soup.find('img', {'itemprop':'thumbnail'})['src']
	def price(self, soup):
		return soup.find('span', {'itemprop':'price'})['content']
			
class cel_parser(Parser):
	def get_url(self):
		if not 'https://www.cel.ro' in self.url:
			return f'https://www.cel.ro{self.url}'
		return self.url
	def title(self, soup):	
		return soup.find(id='product-name').contents[0].strip()
	def photo(self, soup):
		return soup.find(id='main-product-image')['src']
	def price(self, soup):
		return soup.find(id='product-price').contents[0]
		
distribute = {
    'emag': emag_parser,
    'flanco': flanco_parser,
    'cel': cel_parser
}
		
def parse(site, url):
    my_parser = distribute[site](site, url)
    return my_parser.parse()