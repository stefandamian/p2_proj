supported_sites = ['cel', 'flanco', 'emag']

spacing = {
	'emag': '%20',
	'flanco': '+',
	'cel': '+'
	}
	
search_url = {
	'emag': 'https://www.emag.ro/search/',
	'flanco': 'https://www.flanco.ro/catalogsearch/result/?q=',
	'cel': 'https://www.cel.ro/cauta/'
}

validare = {
	'emag': ('span', {'class':'title-phrasing title-phrasing-sm text-danger'}),
	'flanco': ('div', {'class':'acc-warn'}),
	'cel': ('div', {'class':'inexistenta2027'})
}

containter_produse = {
	'emag': {'id': 'card_grid'},
	'flanco':{'id': 'products-wrapper'},
	'cel': {
		'name': 'div', 
		'attrs': {'class':'productlisting'}}
}

containter_produs = {
	'emag': ('div', {'class':'card-item js-product-data'}),
	'flanco': ('div', {'class':'produs'}),
	'cel': ('div', {'class':'product_data productListing-tot'})
}

link_produs = {
	'emag': ('a', {'class': 'thumbnail-wrapper js-product-url'}),
	'flanco': ('a', {'class': 'product-new-link'}),
	'cel': ('a', {'class': 'productListing-data-b product_link product_name'})
}