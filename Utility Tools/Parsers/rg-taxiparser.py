# -*- coding: utf-8 -*-
"""
"""

import io
import csv
import reverse_geocoder as rg
from datetime import datetime

# Sets our own zip code data
geo = rg.RGeocoder(mode=1, verbose=True, stream=io.StringIO(open('census_zip.csv', encoding='utf-8').read()))

def getZips(coordinates):
    return geo.query(coordinates)

# Cleans time from datetime
# Reformats date to match NYPD complaint data
def cleanDate(string):
    date = string[:10]
    date = string[5:7] + "/" + string[8:10] + "/" + string[0:4]
    return date

def writeRows_TDP(numRows, dates, result, outputCSV):
    for x in range(0, numRows):
        outRow = [dates[x], result[2*x]['name'], result[2*x+1]['name']]
        outputCSV.writerow(outRow)
       
def taxiDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            batch_query_size = 1000000
            taxiData = csv.DictReader(csvfile, delimiter = ',')
            print(taxiData)
            outputCSV = csv.writer(outfile, delimiter = ',')
            outputCSV.writerow(['date', 'pickup_zipcode', 'dropoff_zipcode'])
            g_count = 0
            l_count = 0
            coor_list = []
            dates = []
            for row in taxiData:
                pLong = float(row['pickup_longitude'])
                pLat = float(row['pickup_latitude'])
                dLong = float(row['dropoff_longitude'])
                dLat = float(row['dropoff_latitude'])
                # Skips rows that have 0 for latitude and longitude
                if (pLong != 0.0) and (pLat != 0.0) and (dLong != 0.0) and (dLat != 0.0):
                    date = str(row['pickup_datetime'])
                    date = cleanDate(date)
                    dates.append(date)
                    coor_list.append((pLat,pLong))
                    coor_list.append((dLat,dLong))
                    l_count += 1
                    g_count += 1
                    if (l_count >= batch_query_size):
                        result = getZips(coor_list)
                        writeRows_TDP(l_count, dates, result, outputCSV)
                        dates = []
                        coor_list = []
                        print(" -> Processed ", l_count, " rows")
                        l_count = 0
            result = getZips(coor_list)
            writeRows_TDP(l_count, dates, result,outputCSV)
            print(" -> Processed ", l_count, " rows")


startTime = datetime.now()
taxiDataParser("--INPUT-FILE--", "--OUTPUT-FILE--")
print(datetime.now() - startTime)