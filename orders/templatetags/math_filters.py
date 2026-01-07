from django import template

register = template.Library()

@register.filter
def mul(a, b):
    try:
        return a * b
    except:
        return 0
