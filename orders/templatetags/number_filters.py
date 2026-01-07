from django import template

register = template.Library()

PERSIAN_DIGITS = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

@register.filter
def to_persian(value):
    value = str(value)
    for en, fa in PERSIAN_DIGITS.items():
        value = value.replace(en, fa)
    return value
