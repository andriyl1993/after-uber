import json

from django.http import HttpResponse

def address_validator(fn):

	def wrapper(request):
		data = request.POST
		if data.get('start') and 'end' in data.get('end'):
			return fn(request)
		else:
			return HttpResponse(json.dumps({'result': 'error'}))

	return wrapper
