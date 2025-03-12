from django import template

register = template.Library()

@register.filter
def has_errors(error_list):
    if error_list:
        return 'true'
    else:
        return 'false'