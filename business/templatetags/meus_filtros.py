from django import template

register = template.Library()

@register.filter
def get_item(dicionario, chave):
    return dicionario.get(chave)