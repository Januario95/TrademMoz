from django import template

register = template.Library()


@register.filter
def replace_value(value):
	return value.replace(' ', '_')

