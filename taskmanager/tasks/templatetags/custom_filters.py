from django import template

register = template.Library()

@register.filter(name='split_last')
def split_last(value, sep):
    parts = value.rsplit(sep, 1)
    return parts[-1] if len(parts) > 1 else value
