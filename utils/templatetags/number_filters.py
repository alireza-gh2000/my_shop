from django import template

register = template.Library()

@register.filter
def three_digits(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", "،")
    except:
        return value
