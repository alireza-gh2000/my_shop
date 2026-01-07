from django import template

register = template.Library()

_p_map = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

@register.filter
def price_fa(value):
    """
    1234567 -> ۱٬۲۳۴٬۵۶۷ تومان
    """
    if value is None:
        return ''

    try:
        value = int(value)
    except:
        return value

    formatted = f"{value:,}".replace(',', '٬')
    return formatted.translate(_p_map) + ' تومان'
