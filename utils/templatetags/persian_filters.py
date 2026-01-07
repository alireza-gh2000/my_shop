from django import template

register = template.Library()

persian_digits = {
    "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴",
    "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹"
}

def to_persian_numbers(value):
    return ''.join(persian_digits.get(ch, ch) for ch in str(value))

@register.filter
def persian_thousand(value):
    try:
        value = int(value)
        value = f"{value:,}".replace(",", "،")
        return to_persian_numbers(value)
    except:
        return value
