from django import template
from datetime import datetime

register = template.Library()

@register.filter
def to_date(timestamp):
    try:
        return datetime.fromtimestamp(timestamp)
    except AttributeError as error:
        pass