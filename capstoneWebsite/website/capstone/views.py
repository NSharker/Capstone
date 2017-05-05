from django.shortcuts import render
from pymongo import MongoClient

# Create your views here.
def index(request):
	client = MongoClient('127.0.0.1', 27017)
	db = client['househunter']
	collection = db.historicaldata
	data = list(collection.find({'date_enc':0}, {'_id':0}))
	return render(request, 'capstone/home.html', {'data':data})