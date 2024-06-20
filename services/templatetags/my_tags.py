import datetime
from django import template

import random
import string

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


# Создание тега
# После добавления модуля templatetags необходимо перезагрузить сервер,
# прежде чем вы сможете использовать теги или фильтры в шаблонах.


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def time_until_11_nov():
    now = datetime.datetime.today()
    present_year = now.year

    if now > datetime.datetime(present_year, 11, 11):
        present_year += 1

    eleven_eleven = datetime.datetime(present_year, 11, 11)
    d = eleven_eleven - now  # str(d)  '83 days, 2:43:10.517807'
    mm, ss = divmod(d.seconds, 60)
    hh, mm = divmod(mm, 60)

    return "До распродажи 11.11 осталось: {} дней".format(d.days)
    # return 'До распродажи 11.11 осталось: {} дней {} часа {} мин {} сек.'.format(d.days, hh, mm, ss)


# Создание фильтра
@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = "<strong>%s</strong>%s" % (esc(first), esc(other))
    return mark_safe(result)


# Создание тега
@register.simple_tag
def generate_fake_mail(length: int = "10"):
    # length = int(s_length)
    letters = string.ascii_letters + string.digits  # + string.punctuation
    mail = "".join(random.choice(letters) for _ in range(length))

    letters2 = string.ascii_lowercase
    mail2 = "".join(random.choice(letters2) for _ in range(length // 2))
    return f"{mail}@{mail2}.com"


# Создание фильтра
@register.filter
def last_five_contacts(query_set):
    number = len(query_set)
    if number <= 5:
        return query_set
    else:
        return query_set[number - 5 : number + 1]


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"

    return "/static/image/no_image.png"
