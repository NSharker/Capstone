# -*- coding: utf-8 -*-
"""

@author: Nishad
"""
import csv

from geopy.distance import great_circle
from datetime import datetime


'''import geopy

from geopy.geocoders import Nominatim
'''

'''
def complaintDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        complaintData = csv.reader(csvfile, delimiter=',')
        number = 0
        for row in complaintData:
            for i in row:
                print ("slot: " + i +" = ")
            number += 1
            print (number)
            if (number > 4):
                break
                
        
                
                
                
                
                
def complaintDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            number = 0
            for row in complaintData:
                outRow = [row['RPT_DT'], row['LAW_CAT_CD'], row['Latitude'], row['Longitude']]
                outputCSV.writerow(outRow)
                number += 1
                print (number)
                if (number > 4):
                    break

               
'''

'''
def longLatToZipCode(latitude, longitude, minZip = 10001, maxZip = 11697):
    """Returns the string of the zip code located at the latitude and longitude
        latitude = the latitude point
        longitude = the longitude point
        minZip = the minimum value that the zipcode can be, 10001 in NYC
        maxZip = the maximum value the zipcode can be, 11697 in NYC  
    """
    geolocator = Nominatim()
    latLongString = latitude + "," + longitude
    location = geolocator.reverse(latLongString)
    addressString = location.address
    listOfItems = addressString.split(", ")
    for i in listOfItems:
        if i.isdigit() and int(i) >= minZip and int(i) <= maxZip:
            return i
'''
'''
def complaintDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            outputCSV.writerow(['RPT_DT','LAW_CAT_CD','Latitude','Longitude'])
            for row in complaintData:
                outRow = [row['RPT_DT'], row['LAW_CAT_CD'], row['Latitude'], row['Longitude']]
                outputCSV.writerow(outRow)

'''

# Finds shortest ZIP code closest to coordinates

def getZip(lat, long, data):
    coor = (lat, long)
    short = 1000000
    for key, value in data.items():
        baseLat = float(value['Lat'])
        baseLong = float(value['Long'])
        baseCoor = (baseLat, baseLong)
        dist = great_circle(baseCoor, coor).miles
        if abs(dist) < short:
            short = dist
            zipCode = key
    return zipCode

# Opens csv with ZIP codes and coordinates
# Returns it as a dictionary

def getZipDict(inputFileName):
    with open(inputFileName, 'r') as csvfile:
        zipDict = csv.DictReader(csvfile, delimiter = ',')
        result = {}
        for row in zipDict:
            key = row.pop('Zip')
            result[key] = row
        return result

# Parses Taxi Data
# Needs input file, output file, and dictionary of ZIP codes




'''
def complaintDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            outputCSV.writerow(['RPT_DT','LAW_CAT_CD','ZIPCODE'])
            for row in complaintData:
                if row['Latitude'] and row['Longitude']:
                    zipCode = longLatToZipCode(row['Latitude'], row['Longitude'])
                    outRow = [row['RPT_DT'], row['LAW_CAT_CD'], zipCode]
                    outputCSV.writerow(outRow)
'''

                    
def complaintDataParser(inputFileName, outputFileName, data):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            outputCSV.writerow(['RPT_DT','LAW_CAT_CD','ZIPCODE'])
            for row in complaintData:
                if row['Latitude'] and row['Longitude']:
                    long = float(row['Longitude'])
                    lat = float(row['Latitude'])
                    zipCode = getZip(lat, long, data)
                    outRow = [row['RPT_DT'], row['LAW_CAT_CD'], zipCode]
                    outputCSV.writerow(outRow)



'''
def taxiDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            outputCSV.writerow(['pickup_datetime','dropoff_datetime','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count'])
            for row in complaintData:
                outRow = [row['pickup_datetime'], row['dropoff_datetime'], row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'], row['dropoff_latitude'], row['passenger_count']]
                outputCSV.writerow(outRow)
'''
        
zipDict = getZipDict("ny_zip_coords.csv")
complaintDataParser("NYPD_Complaint_Data_Historic.csv","outputComplaintIden.csv", zipDict)


#taxiDataParser("yellow_tripdata_2010-01.csv", "yellow2010output.csv")
        


def taxiDataParser(inputFileName, outputFileName, data):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            taxiData = csv.DictReader(csvfile, delimiter = ',')
            outputCSV = csv.writer(outfile, delimiter = ',')
            outputCSV.writerow(['pickup_datetime', 'dropoff_datetime', 'pickup_zipcode', 'dropoff_zipcode', 'passenger_count'])
            count = 0
            for row in taxiData:
                pLong = float(row['pickup_longitude'])
                pLat = float(row['pickup_latitude'])
                if (pLong != 0) and (pLat != 0):
                    dLong = float(row['dropoff_longitude'])
                    dLat = float(row['dropoff_latitude'])
                    shortPickZip = getZip(pLat, pLong, data)
                    shortDropZip = getZip(dLat, dLong, data)
                    if (shortPickZip != 0) or (shortDropZip != 0):
                        outRow = [row['pickup_datetime'], row['dropoff_datetime'], shortPickZip, shortDropZip, row['passenger_count']]
                        outputCSV.writerow(outRow)
                count += 1
                if count % 1000000 == 0:
                    print("Processed ", count, " entries.")
        
        
        
        
        
        
        
        
        
        
        #with open(outputFileName, 'wb') as writecsvfile:
         #   writer = csv.writer(writecsvfile)
          #  for row in complaintData:
            