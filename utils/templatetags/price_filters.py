from django import template

register = template.Library()

@register.filter
def price_format(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", "،")
    except:
        return value

@register.filter
def toman(value):
    try:
        value = int(value)
        formatted = f"{value:,}".replace(",", "،")
        return f"{formatted} تومان"
    except:
        return value
