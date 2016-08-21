import json

from django.http import HttpResponse

def address_validator(fn):

	def wrapper(request):
		data = request.POST
		if 'start' in data and 'end' in data:
			return fn(request)
		else:
			return HttpResponse({'result': 'error'})

	return wrapper
