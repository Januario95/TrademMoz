from django import template

register = template.Library()


@register.filter
def replace_value(value):
	return value.replace(' ', '_')

@register.filter
def replace_value2(value):
	return value.replace(' ', '-').replace('_', '-').lower()[::-1]

@register.filter
def remove_zeros(value):
	value = str(value).split('.')
	value = value[0] + '.' + value[1][:2]
	return value

@register.filter
def format_none(value):
	if value is None:
		return '-'
	return f'{value}%'


