import io
import csv
import reverse_geocoder as rg
from datetime import datetime

# TODO: Fix ny_zip_coords.csv. Maybe taking the information from zips.csv (from sourceforge)
# Entire zips.csv (and outside NYC) included as zips_coord.csv. 
# TODO: Remove quotes from lat_long and zipcodes with letters
geo = rg.RGeocoder(mode=2, verbose=True, stream=io.StringIO(open('ny_zip_coords.csv', encoding='utf-8').read()))

def getZips(coordinates):
    return geo.query(coordinates)

def writeRows_TDP(numRows, needed_Info, result, outputCSV):
    for x in range(0, numRows):
        outRow = [needed_Info[x][0], needed_Info[x][1], result[2*x]['name'], result[2*x+1]['name'], needed_Info[x][2]]
        outputCSV.writerow(outRow)

def taxiDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
    	with open(outputFileName, 'w', newline = '') as outfile:
    		batch_query_size = 5000000
    		taxiData = csv.DictReader(csvfile, delimiter = ',')
    		print(taxiData)
    		outputCSV = csv.writer(outfile, delimiter = ',')
    		outputCSV.writerow(['pickup_datetime', 'dropoff_datetime', 'pickup_zipcode', 'dropoff_zipcode', 'passenger_count'])
    		g_count = 0
    		l_count = 0
    		coor_list = []
    		needed_Info = []
    		for row in taxiData:
    			pLong = row['pickup_longitude']
    			pLat = row['pickup_latitude']
    			dLong = row['dropoff_longitude']
    			dLat = row['dropoff_latitude']
    			if (pLong != "") and (pLat != "") and (dLong != "") and (dLat != ""):
    				needed_Info.append( [row['pickup_datetime'], row['dropoff_datetime'], row['passenger_count']] )
    				coor_list.append((float(pLat),float(pLong)))
    				coor_list.append((float(dLat),float(dLong)))
    				l_count += 1
    				g_count += 1
    				if (l_count >= batch_query_size):
    					result = getZips(coor_list)
    					writeRows_TDP(l_count, needed_Info, result, outputCSV)
    					needed_Info = []
    					coor_list = []
    					print(" -> Processed ", l_count, " rows")
    					l_count = 0
    		result = getZips(coor_list)
    		writeRows_TDP(l_count,needed_Info,result,outputCSV)
    		print(" -> Processed ", l_count, " rows")


startTime = datetime.now()
taxiDataParser("-INPUT-FILE-NAME-", "-OUTPUT-FILE-NAME-")
print(datetime.now() - startTime)
