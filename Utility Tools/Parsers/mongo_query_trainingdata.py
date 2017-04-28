from pymongo import MongoClient

# In: Query = Dictionary of key values to match in DB
# Out: List of all results found
def query_trainingdata(query):
	# Init Client
	client = MongoClient('localhost', 27017)

	# Select Database Name
	db = client.househunter
	# Same as above
	# db = client['househunter']

	# Select collection of data, historicaldata
	collection = db.historicaldata

	# Put every document result in a list and return it
	result = []
	for doc in collection.find(query):
		result.append(doc)
	return result