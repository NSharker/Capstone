# -*- coding: utf-8 -*-
"""
"""

import io
import csv
import reverse_geocoder as rg
from datetime import datetime

# Sets our own zip code data
geo = rg.RGeocoder(mode=1, verbose=True, stream=io.StringIO(open('ny_zip_coords_fixed.csv', encoding='utf-8').read()))

def getZips(coordinates):
    return geo.query(coordinates)

# Cleans time from datetime
# Reformats date to match NYPD complaint data
def cleanDate(string):
    date = string[:10]
    date = string[5:7] + "/" + string[8:10] + "/" + string[0:4]
    return date

def writeRows_TDP(numRows, neededInfo, result, outputCSV):
    for x in range(0, numRows):
        date = cleanDate(str(neededInfo[x][0]))
        outRow = [date, result[2*x]['name'], result[2*x+1]['name'], neededInfo[x][1]]
        outputCSV.writerow(outRow)
        
def writeRows_CDP(numRows, neededInfo, result, outputCSV):
    for x in range(0, numRows):
        #date = cleanDate(str(neededInfo[x][0]))
        outRow = [neededInfo[x][0], result[x]['name'], neededInfo[x][1]]
        outputCSV.writerow(outRow)
       
def taxiDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            batch_query_size = 1000000
            taxiData = csv.DictReader(csvfile, delimiter = ',')
            print(taxiData)
            outputCSV = csv.writer(outfile, delimiter = ',')
            outputCSV.writerow(['date', 'pickup_zipcode', 'dropoff_zipcode', 'passenger_count'])
            g_count = 0
            l_count = 0
            coor_list = []
            neededInfo = []
            for row in taxiData:
                pLong = row['pickup_longitude']
                pLat = row['pickup_latitude']
                dLong = row['dropoff_longitude']
                dLat = row['dropoff_latitude']
                # Skips rows that have empty entries for latitude and longitude
                if (pLong != '') and (pLat != '') and (dLong != '') and (dLat != ''):
                    pLong = float(pLong)
                    pLat = float(pLat)
                    dLong = float(dLong)
                    dLat = float(dLat)
                # Skips rows that have 0 for latitude and longitude
                    if (pLong != 0.0) and (pLat != 0.0) and (dLong != 0.0) and (dLat != 0.0):
                        neededInfo.append([row['pickup_datetime'], row['passenger_count']])
                        coor_list.append((pLat,pLong))
                        coor_list.append((dLat,dLong))
                        l_count += 1
                        g_count += 1
                        if (l_count >= batch_query_size):
                            result = getZips(coor_list)
                            writeRows_TDP(l_count, neededInfo, result, outputCSV)
                            neededInfo = []
                            coor_list = []
                            print(" -> Processed ", l_count, " rows")
                            l_count = 0
            result = getZips(coor_list)
            writeRows_TDP(l_count, neededInfo, result,outputCSV)
            print(" -> Processed ", l_count, " rows")

            
            
            
def complaintDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            batch_query_size = 1000000
            complaintData = csv.DictReader(csvfile, delimiter = ',')
            print(inputFileName)
            outputCSV = csv.writer(outfile, delimiter = ',')
            outputCSV.writerow(['date', 'zipcode', 'law_cat_cd'])
            g_count = 0
            l_count = 0
            coor_list = []
            neededInfo = []
            for row in complaintData:
                pLong = row['Longitude']
                pLat = row['Latitude']
                # Skips rows that have empty entries for latitude and longitude
                if (pLong != '') and (pLat != ''):
                    pLong = float(pLong)
                    pLat = float(pLat)
                # Skips rows that have 0 for latitude and longitude
                    if (pLong != 0.0) and (pLat != 0.0):
                        neededInfo.append([row['RPT_DT'], row['LAW_CAT_CD']])
                        coor_list.append((pLat,pLong))
                        l_count += 1
                        g_count += 1
                        if (l_count >= batch_query_size):
                            result = getZips(coor_list)
                            writeRows_CDP(l_count, neededInfo, result, outputCSV)
                            neededInfo = []
                            coor_list = []
                            print(" -> Processed ", l_count, " rows")
                            l_count = 0
            result = getZips(coor_list)
            writeRows_CDP(l_count, neededInfo, result,outputCSV)
            print(" -> Processed ", l_count, " rows")

'''
startTime = datetime.now()
#taxiDataParser("--INPUT-FILE--", "--OUTPUT-FILE--")
taxiDataParser("C:/Users/Nishad/Desktop/Data/green_tripdata_2015-01.csv", "C:/Users/Nishad/Desktop/Data/Cleaned/green_tripdata_2015-01Cleaned.csv")

print(datetime.now() - startTime)            

startTime = datetime.now()
taxiDataParser("--INPUT-FILE--", "--OUTPUT-FILE--")
print(datetime.now() - startTime)
