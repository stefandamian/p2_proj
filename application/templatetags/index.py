from django import template

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

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
    
    
