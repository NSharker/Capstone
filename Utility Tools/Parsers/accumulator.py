# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:15:35 2017

@author: Nishad
"""
import csv
from datetime import datetime

            
def taxiDataAccumulator(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            taxiData = csv.DictReader(csvfile, delimiter = ',')
            pickUpAccumulation = {}
            dropOffAccumulation = {}
            pickUpPassengersAccumulation = {}
            dropOffPassengersAccumulation = {}
            firstRow = next(taxiData)
            date = firstRow['date'][0:2] + "/"+ firstRow['date'][6:]
            pickUpAccumulation[firstRow['pickup_zipcode']] = 1
            dropOffAccumulation[firstRow['dropoff_zipcode']] = 1
            pickUpPassengersAccumulation[firstRow['pickup_zipcode']] = int(firstRow['passenger_count'])
            dropOffPassengersAccumulation[firstRow['dropoff_zipcode']] = int(firstRow['passenger_count'])

            
            for row in taxiData:
                if row['pickup_zipcode'] in pickUpAccumulation:
                    pickUpAccumulation[row['pickup_zipcode']] += 1
                else:
                    pickUpAccumulation[row['pickup_zipcode']] = 1
                if row['dropoff_zipcode'] in dropOffAccumulation:
                    dropOffAccumulation[row['dropoff_zipcode']] +=1
                else:
                    dropOffAccumulation[row['dropoff_zipcode']] = 1
                if row['pickup_zipcode'] in pickUpPassengersAccumulation:
                    pickUpPassengersAccumulation[row['pickup_zipcode']] += int(row['passenger_count'])
                else:
                    pickUpPassengersAccumulation[row['pickup_zipcode']] = int(row['passenger_count'])
                if row['dropoff_zipcode'] in dropOffPassengersAccumulation:
                    dropOffPassengersAccumulation[row['dropoff_zipcode']] += int(row['passenger_count'])
                else:
                    dropOffPassengersAccumulation[row['dropoff_zipcode']] = int(row['passenger_count'])

                
            outPutCSV = csv.writer(outfile,delimiter = ',')
            outPutCSV.writerow(['date','zipcode','pickups','dropoffs','pickup_passengers','dropoff_passengers'])
            keysInPickUp = list(pickUpAccumulation.keys())
            
            for keyP in keysInPickUp:
                zipCode = keyP
                pickUpNumber = pickUpAccumulation.pop(keyP)
                if keyP in dropOffAccumulation:
                    dropOffNumber = dropOffAccumulation.pop(keyP)
                else:
                    dropOffNumber = 0
                pickUpPassengerNumber = pickUpPassengersAccumulation.pop(keyP)
                if keyP in dropOffPassengersAccumulation:
                    dropOffPassengerNumber = dropOffPassengersAccumulation.pop(keyP)
                else:
                    dropOffPassengerNumber = 0
                outPutCSV.writerow([date, zipCode, pickUpNumber, dropOffNumber, pickUpPassengerNumber, dropOffPassengerNumber])
                
            keysInDropOff = list(dropOffAccumulation.keys())
            
            for keyD in keysInDropOff:
                zipCode = keyD
                dropOffNumber = dropOffAccumulation.pop(keyD)
                pickUpNumber = 0
                dropOffPassengerNumber = dropOffPassengersAccumulation.pop(keyD)
                pickUpPassengerNumber = 0
                outPutCSV.writerow([date,zipCode,pickUpNumber, dropOffNumber, pickUpPassengerNumber, dropOffPassengerNumber])
            
                
                
            
            
            
startTime = datetime.now()        
taxiDataAccumulator("C:/Users/Nishad/Desktop/Data/Cleaned/yellow_tripdata_2015-01Cleaned.csv","C:/Users/Nishad/Desktop/Data/Cleaned/Accumlated/yellow_tripdata_2015-01Accum.csv")
print(datetime.now() - startTime)        

            
    