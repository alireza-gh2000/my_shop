from django import template
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value, fmt="%Y/%m/%d %H:%M"):
    """
    تبدیل datetime گِرِگوری به رشته‌ی تاریخ شمسی.
    استفاده در قالب: {{ some_datetime|to_jalali:"%Y/%m/%d" }}
    """
    if not value:
        return ""
    try:
        # jdatetime expects a python datetime object
        jdt = jdatetime.datetime.fromgregorian(datetime=value)
        return jdt.strftime(fmt)
    except Exception:
        return value
