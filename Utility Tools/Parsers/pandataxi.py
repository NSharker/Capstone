import pandas as pd
import time
from geopy.distance import great_circle
from datetime import datetime

taxi_file = "../../output.csv"
ny_file = "ny_zip_coords.csv"
destination_file = "../../output_zip.csv"

def getZip(lat, long, data):
    coor = (lat, long)
    short = 1000000
    for index, row in data.iterrows():
    	dist = great_circle((row.Lat, row.Long), coor).miles
    	if abs(dist) < short:
    		short = dist
    		zipCode = row.Zip
    return zipCode

seconds1 =  0
seconds1 = seconds1 - time.time()

print("Reading :", taxi_file)
d1 = pd.read_csv(taxi_file)

print("Reading :", taxi_file)
data = pd.read_csv(ny_file)

print("Creating : dropoff_zipcode column in df")
d1['dropoff_zipcode'] = 'None'

print("Creating : pickup_zipcode column in df")
d1['pickup_zipcode'] = 'None'

print("Calculating Zipcode")
count = 0
for index, row in d1.iterrows():
	row.pickup_zipcode = getZip(row.pickup_latitude, row.pickup_longitude, data)
	row.dropoff_zipcode = getZip(row.dropoff_latitude, row.dropoff_longitude, data)
	count += 1
    # UNCOMMENT to print every x number of lines
	#if (count % 100000 == 0):
	print("->Computed ", count)

print("Deleting pickup and dropoff long | lat columns")
d1.pop('pickup_longitude')
d1.pop('pickup_latitude')
d1.pop('dropoff_longitude')
d1.pop('dropoff_latitude')

print("Dumping to new csv: ", )
d1.to_csv(destination_file)

seconds1 = seconds1 + time.time()
print("Program took %d seconds.", seconds1)


