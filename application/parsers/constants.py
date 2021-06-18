supported_sites = ['cel', 'flanco', 'emag', 'pcGarage']#, 'mediaGalaxy'] #, 'altex']

spacing = {
	'emag': '%20',
	'flanco': '+',
	'cel': '+',
	'altex': '%2520',
	'mediaGalaxy': '%2520',
	'pcGarage': '+',
	}
	
search_url = {
	'emag': 'https://www.emag.ro/search/',
	'flanco': 'https://www.flanco.ro/catalogsearch/result/?q=',
	'cel': 'https://www.cel.ro/cauta/',
	'altex': 'https://www.altex.ro/cauta/?q=',
	'mediaGalaxy': 'https://mediagalaxy.ro/cauta/?q=',
	'pcGarage': 'https://www.pcgarage.ro/cauta/',
}

validare = {
	'emag': ('span', {'class':'title-phrasing title-phrasing-sm text-danger'}),
	'flanco': ('div', {'class':'message notice'}),
	'cel': ('div', {'class':'inexistenta2027'}),
	'mediaGalaxy': ('div', {'class':'border flex items-center text-usm p-3 rounded text-alertYellow bg-alertYellow-bg border-alertYellow-border'}),
	'altex': ('div', {'class':'border flex items-center text-usm p-3 rounded text-alertYellow bg-alertYellow-bg border-alertYellow-border'}),
	'pcGarage': ('div', {'class':'inexistenta2027'}),
}

containter_produse = {
	'emag': {'id': 'card_grid'},
	'flanco':{
		'name': 'ol', 
		'attrs': {'class' : 'products list items product-items'}},
	'cel': {
		'name': 'div', 
		'attrs': {'class':'productlisting'}},
	'mediaGalaxy': {
		'name': 'ul',
		'attrs': {'class':'Products Products--grid Products--4to2'}},
	'altex': {
		'name': 'ul',
		'attrs': {'class':'Products Products--grid Products--4to2'}},
	'pcGarage': {'id': 'wrapper_listing_products'}
}

containter_produs = {
	'emag': ('div', {'class':'card-item js-product-data'}),
	'flanco': ('div', {'class':'product-item-info'}),
	'cel': ('div', {'class':'product_data productListing-tot'}),
	'mediaGalaxy': ('div', {'class': 'Product'}),
	'altex': ('div', {'class': 'Product'}),
	'pcGarage': ('div', {'class': 'product_box'}),
}

link_produs = {
	'emag': ('a', {'class': 'thumbnail-wrapper js-product-url'}),
	'flanco': ('a', {'class': 'product photo product-item-photo'}),
	'cel': ('a', {'class': 'productListing-data-b product_link product_name'}),
	'altex': ('a', {'class': 'Product-name'}),
	'mediaGalaxy': ('a', {'class': 'Product-name'}),
	'pcGarage': ('a')
}