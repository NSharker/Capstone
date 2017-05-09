from pymongo import MongoClient
import pandas as pd

# Read Dataframe
data = pd.read_csv("final_trainingdata.csv")

# Delete extra columns
del data["Unnamed: 0"]
del data["Unnamed: 0.1"]

# Convert to list of rows in dictionary format
data_dict = data.to_dict(orient='records')

# Init Client
client = MongoClient('localhost', 27017)

# Select Database Name
db = client.househunter
# Same as above
# db = client['househunter']

# Select collection of data, historicaldata
collection = db.historicaldata

# Insert all the data
collection.insert_many(data_dict)