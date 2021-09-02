import os

from django import template

register = template.Library()


@register.simple_tag
def get_img_url(obj, size):
    file, ext = os.path.splitext(obj.img.url)
    return f'{file}_{size}{ext}'
