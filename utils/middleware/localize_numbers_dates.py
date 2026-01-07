import re
from bs4 import BeautifulSoup, NavigableString, Tag
from django.utils.deprecation import MiddlewareMixin
import jdatetime
from datetime import datetime

eng_digits = "0123456789"
fa_digits  = "۰۱۲۳۴۵۶۷۸۹"
trans_table = str.maketrans(eng_digits, fa_digits)

DATE_RE = re.compile(r'\b(20\d{2}|19\d{2})[\/\-.](0?[1-9]|1[0-2])[\/\-.](0?[1-9]|[12]\d|3[01])\b')


def en_to_fa(s):
    return s.translate(trans_table)


def format_price(num_str):
    """ سه‌رقمی کردن مخصوص قیمت‌ها """
    try:
        n = int(num_str)
        return "{:,}".format(n)
    except:
        return num_str


def g_to_j(match):
    y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        g = datetime(y, m, d)
        j = jdatetime.date.fromgregorian(date=g.date())
        return f"{j.year}/{j.month:02d}/{j.day:02d}"
    except:
        return match.group(0)


def skip_tag(tag: Tag):
    return tag.name in {"script", "style", "code", "pre", "textarea", "input"}


class LocalizeNumbersDatesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        ct = response.get('Content-Type', '')
        if "text/html" not in ct:
            return response

        try:
            soup = BeautifulSoup(response.content, "html.parser")

            # ---- سه‌رقمی کردن فقط قیمت‌ها ----
            for price_tag in soup.select(".price"):
                if price_tag.string:
                    cleaned = re.sub(r"[^\d]", "", price_tag.string)
                    price_tag.string = format_price(cleaned)

            # ---- فارسی‌سازی اعداد کل سایت ----
            for elem in soup.find_all(string=True):
                parent = elem.parent
                if parent and isinstance(elem, NavigableString):
                    if not skip_tag(parent):
                        new = en_to_fa(str(elem))
                        if new != str(elem):
                            elem.replace_with(new)

            # ---- تبدیل تاریخ ----
            html = str(soup)
            html = DATE_RE.sub(lambda m: g_to_j(m), html)

            response.content = html.encode(response.charset or 'utf-8')

        except Exception as e:
            print("Middleware Error:", e)

        return response
