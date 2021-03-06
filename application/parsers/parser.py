from abc import ABC, abstractmethod
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time

# 

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
				req = Request(self.get_url(), headers={'User-Agent': 'Mozilla/5.0'})
				web = urlopen(req)
				request_done = True
			except:
				time.sleep(1)
				no_time = no_time + 1
		if not request_done:
			print(f'[WARNING] Failed to get request from {self.get_url()}')
			raise ExceptionParseFail(self.get_url(), 'Request not possible site: X')
		if web.getcode() != 200:
			raise Exception(f'Return code from site {web.getcode()}')
		
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
		if self.site == 'emag':
			time.sleep(2)
		while((not request_done) and (no_time < 2)):
			try:
				req = Request(self.get_url(), headers={'User-Agent': 'Mozilla/5.0'})
				web = urlopen(req)
				request_done = True
			except:
				time.sleep(1)
				no_time = no_time + 1
		if not request_done:
			raise ExceptionParseFail(self.get_url(), 'Request not possible site: X')
		if web.getcode() != 200:
			raise Exception(f'Return code from site {web.getcode()}')
		
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
			try:			
				value = float(f"{p1}.{p[1].contents[0]}")
			except ValueError:
				pass
			else:
				return value
		raise ExceptionParseFail(self.url)
			
class flanco_parser(Parser):
	def title(self, soup):	
		result = soup.find('span', {'itemprop':'name', 'data-ui-id':'page-title-wrapper'}) 
		if result != None:
			return result.contents[0].strip()
		raise ExceptionParseFail(self.url)
	def photo(self, soup):
		result = soup.find('img', {'itemprop':'thumbnail'})
		if result != None:
			return result['src']
		raise ExceptionParseFail(self.url)
	def price(self, soup):
		result = soup.find('div', {'class': 'product-info-price'})
		if result != None:
			result = result.find('div', {'class': 'price-box price-final_price'})
			if result != None:
				result = result.find('span', {'class':'special-price'})
				if result != None:
					result = result.find('span', {'class':'price'})
					return result.contents[0].replace('.', '').replace(',', '')
				else:
					result = soup.find('div', {'class': 'product-info-price'}).find('div', {'class': 'price-box price-final_price'}).find('span', {'class':'price'})
					if result != None:
						return result.contents[0].replace('.', '').replace(',', '')
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
		
class pcGarage_parser(Parser):
	def title(self, soup):	
		result = soup.find(id='product_name')
		if result != None:
			return result.contents[0].strip()
		raise ExceptionParseFail(self.url)
	def photo(self, soup):
		result = soup.find('div', {'id':'product_media'})
		if result != None:
			result = soup.find('img', {'itemprop':'image'})
			if result != None:
				return result['src']
		raise ExceptionParseFail(self.url)
	def price(self, soup):
		result = soup.find('meta', {'itemprop':'price'})
		if result != None:
			return "{:.2f}".format(float(result['content']))
		raise ExceptionParseFail(self.url)
            
distribute = {
    'emag': emag_parser,
    'flanco': flanco_parser,
    'cel': cel_parser,
    'pcGarage': pcGarage_parser,
}
		
def parse(site, url):
    my_parser = distribute[site](site, url)
    return my_parser.parse()

def parse_price(site, url):
	my_parser = distribute[site](site, url)
	return my_parser.parse_price()
