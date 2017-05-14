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
		cus = request.POST.get('cus')
		months = request.POST.get('m')
		years = request.POST.get('y')
		zip = request.POST.get('z')
		if cus == "true":
			cusp = request.POST.get('cusp')
			cuspass = request.POST.get('cuspass')
			cusd = request.POST.get('cusd')
			cusdpass = request.POST.get('cusdpass')
			cusf = request.POST.get('cusf')
			cusm = request.POST.get('cusm')
			cusv = request.POST.get('cusv')
			if cusp == '':
				cusp = 0
			if cuspass == '':
				cuspass = 0
			if cusd == '':
				cusd = 0
			if cusdpass == '':
				cusdpass = 0
			if cusf == '':
				cusf = 0
			if cusm == '':
				cusm = 0
			if cusv == '':
				cusv = 0
			x = ml.predictHousingPrice(int(months), int(years), int(zip), int(cusp), int(cuspass), int(cusd), int(cusdpass), int(cusf), int(cusm), int(cusv))
		else:
			x = ml.predictHousingPrice(int(months), int(years), int(zip))
		x['date'] = (int(years)-2010)*12 + int(months) -1
		return HttpResponse(
			json.dumps(x),
			content_type="application/json"
		)
	return render(request, 'capstone/home.html', {'data':data})