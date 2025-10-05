from django import template

register = template.library()
@register.filter
def get_item(d, key):
    return d.get(key, [])