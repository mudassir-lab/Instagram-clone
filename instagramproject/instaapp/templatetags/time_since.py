from django import template
from datetime import datetime

register = template.Library()


@register.filter
def time_since(value):
    now = datetime.now()
    # print(now)
    diff = now - value

    seconds = diff.total_seconds()

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if days:
        return f"{int(days)} D AGO"
    elif hours:
        return f"{int(hours)} H AGO"
    elif minutes:
        return f"{int(minutes)} M AGO"
    else:
        return f"{int(seconds)} S AGO"
