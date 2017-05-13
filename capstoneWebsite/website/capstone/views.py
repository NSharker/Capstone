from django.shortcuts import render
from pymongo import MongoClient
from django.http import HttpResponse
from . import machinelearning as ml
import json

# Create your views here.
def index(request):
	client = MongoClient('127.0.0.1', 27017)
	db = client['househunter']
	data = []
	collection = db.historicaldata
	for i in range(0, 72):
		data.append(list(collection.find({'date_enc':i}, {'_id':0})))
	if request.method == 'POST':
		months = request.POST.get('m')
		years = request.POST.get('y')
		zip = request.POST.get('z')
		#response_data = {}
		
		#response_data['m'] = months;
		#response_data['y'] = years;
		
		x = ml.predictHousingPrice(int(months), int(years), int(zip))
		return HttpResponse(
			json.dumps(x),
			content_type="application/json"
		)	
	return render(request, 'capstone/home.html', {'data':data})