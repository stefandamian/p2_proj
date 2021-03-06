from django import template

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def length(obj):
    return len(obj)

@register.filter
def nume(obj):
    return obj.nume

@register.filter
def are_preturi(obj):
    return obj.are_preturi()

@register.filter
def pret_initial(obj):
    return obj.pret_initial()

@register.filter
def pret_final(obj):
    return obj.pret_final()

@register.filter
def valoare(obj):
    return obj.valoare
    
@register.filter
def data_creare(obj):
    return obj.data_creare
    
@register.filter
def emag(obj):
    return obj['emag']
    
@register.filter
def flanco(obj):
    return obj['flanco']
    
@register.filter
def cel(obj):
    return obj['cel']
    
@register.filter
def title(obj):
    return obj['title']
    
@register.filter
def photo(obj):
    return obj['photo']
    
@register.filter
def price(obj):
    return obj['price']

@register.filter
def url(obj):
    return obj['url']
    
@register.filter
def site(obj):
    return obj['site']
    
@register.filter
def capitalize(obj):
    return obj.capitalize()
