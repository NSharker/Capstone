# -*- coding: utf-8 -*-
"""

@author: Nishad
"""
import csv

import geopy

from geopy.geocoders import Nominatim

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
tpep_pickup_datetime
tpep_dropoff_datetime
Pickup_longitude
Pickup_latitude
Dropoff_longitude
Dropoff_ latitude
Passenger_count'''

def taxiDataParser(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w') as writecsvfile:
            complaintData = csv.DictReader(csvfile, delimiter=',')
            outputCSV = csv.writer(writecsvfile, delimiter=',')
            outputCSV.writerow(['pickup_datetime','dropoff_datetime','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude','passenger_count'])
            for row in complaintData:
                outRow = [row['pickup_datetime'], row['dropoff_datetime'], row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'], row['dropoff_latitude'], row['passenger_count']]
                outputCSV.writerow(outRow)

        

complaintDataParser("NYPD_Complaint_Data_Historic.csv","output.csv")


#taxiDataParser("yellow_tripdata_2010-01.csv", "yellow2010output.csv")
        
        
        
        
        
'''import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.geocode("175 5th Avenue NYC")
print((location.latitude, location.longitude))
geolocator = Nominatim()
location = geolocator.reverse("
location = geolocator.reverse("40.82884833,-73.91666114")
print(location.address)'''
        
        
        
        
        
        
        
        
        
        
        
        #with open(outputFileName, 'wb') as writecsvfile:
         #   writer = csv.writer(writecsvfile)
          #  for row in complaintData:
            