from pymongo import MongoClient

# Delete all data from collection

# Init Client
client = MongoClient('localhost', 27017)

# Select Database Name
db = client.househunter
# Same as above
# db = client['househunter']

# Select collection of data, historicaldata
collection = db.historicaldata
# Remove all documents in collection
collection.remove({})