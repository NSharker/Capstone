from django.shortcuts import render
from pymongo import MongoClient
from .forms import PostForm
from django.http import HttpResponse
import json
# Create your views here.
def index(request):
	client = MongoClient('127.0.0.1', 27017)
	db = client['househunter']
	collection = db.historicaldata
	data = []
	form = 'Welcome'
	for i in range(0, 72):
		data.append(list(collection.find({'date_enc':i}, {'_id':0})))
	if request.method == 'POST':
		months = request.POST.get('m')
		years = request.POST.get('y')
		response_data = {}
		
		response_data['m'] = months;
		response_data['y'] = years;
		
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)	
	return render(request, 'capstone/home.html', {'data':data})