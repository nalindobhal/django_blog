import math

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name='wordscount', is_safe=True)
@stringfilter
def words_count(value):

    words_list = value.split(' ')
    img_count = value.count('<img')
    time_taken = (len(words_list) / 250) + (img_count / 10)     # time in minutes
    count = math.ceil(time_taken)
    if count > 1:
        return count
    else:
        return 1
