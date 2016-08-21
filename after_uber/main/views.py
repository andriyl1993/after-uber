import json
import requests
import googlemaps

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wrappers import address_validator
from after_uber.settings import CLIENT_ID, CLIENT_SECRET, SERVER_TOKEN, GOOGLE_KEY

def index(request):
	return render(request, 'index.html')

@csrf_exempt
@address_validator
def send(request):
	start = request.POST.get('start')
	end = request.POST.get('end')

	start_coords = get_coords(start)
	end_coords = get_coords(end)

	if 'lat' in start_coords and 'lat' in end_coords:
		response = get_estimate_price(
			start_latitude = start_coords.get('lat'),
			start_longitude = start_coords.get('lng'),
			end_latitude = end_coords.get('lat'),
			end_longitude = end_coords.get('lng'),
		)
	else:
		response = {}

	return HttpResponse(json.dumps(response_data(response)))

def get_coords(address):
	gmaps = googlemaps.Client(key=GOOGLE_KEY)

	geocode_result = gmaps.geocode(address)
	response = geocode_result[0].get('geometry')

	if 'location' in response:
		return response.get('location')
	else:
		return None

def get_estimate_price(start_latitude, start_longitude, end_latitude, end_longitude):
	response = requests.get('https://api.uber.com/v1/estimates/price', params={
		"start_latitude": start_latitude,
		"start_longitude": start_longitude,
		"end_latitude": end_latitude,
		"end_longitude": end_longitude,
		"server_token": SERVER_TOKEN,
	})

	return response.json()

def response_data(data):
	response = {}
	response["result"] = []

	if data.get('prices'):
		response["status"] = "success"
		for price in data.get('prices'):
			response["result"].append({
				"display_name": price.get('display_name') + "After",
				"price": "{0} - {1}".format(int(price.get('low_estimate')) * 0.8, int(price.get('high_estimate')) * 0.8)
			})
	else:
		response["status"] = "error"
	return response
