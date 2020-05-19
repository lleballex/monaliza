from django import template
from ..models import Question

register = template.Library()

def to_array(value):
	print(value)
	try:
		return value.strip().split()
	except:
		return []

register.filter('to_array', to_array)