# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:15:35 2017

@author: Nishad
"""
import csv
import pandas as pd
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
            
# Cuts out day in date field and sorts by month/year. Exports to output        
def sortComplaint(input, output):
    df = pd.read_csv(input)
    df['date'] = df['date'].map(lambda x: str(x)[:3] + str(x)[6:])
    df = df.sort("date")
    df.to_csv(output, index=False)

def complaintDataAccumulator(inputFileName, outputFileName):
    with open(inputFileName, 'r') as csvfile:
        with open(outputFileName, 'w', newline = '') as outfile:
            complaintData = csv.DictReader(csvfile, delimiter = ',')
            #dictionaries with keys = zipcode, and values = accumulated number of events for that month
            felonyAccumulation = {}
            misdemeanorAccumulation = {}
            violationAccumulation = {}
            firstRow = next(complaintData)
            #Use these two variables to check when we switch to a different month/year in our data
            previousDateEntry = firstRow['date'][0:2] + "/"+ firstRow['date'][6:]
            currentDateEntry = previousDateEntry
            #add the data to our accumulation dictionaries based on the law_cat_cd from the first row parsed
            if firstRow['law_cat_cd'] == "FELONY":
                felonyAccumulation[firstRow['zipcode']] = 1
            elif firstRow['law_cat_cd'] == "MISDEMEANOR":
                misdemeanorAccumulation[firstRow['zipcode']] = 1
            elif firstRow['law_cat_cd'] == "VIOLATION":
                violationAccumulation[firstRow['zipcode']] = 1
            else:
                print("MISSING DATA!")
            outPutCSV = csv.writer(outfile,delimiter = ',')
            outPutCSV.writerow(['date','zipcode','FELONIES', 'MISDEMEANORS', 'VIOLATIONS'])
                
            for row in complaintData:
                currentDateEntry = row['date'][0:2] + "/" + row['date'][6:]

                #if previousDateEntry not equal to currentDateEntry then we are in a new month
                if previousDateEntry != currentDateEntry:
                    #write to the output CSV file, all our values in our dictionary
                    keysInFelony = list(felonyAccumulation.keys())
                    #write all the zipcodes found in the felony dictionary
                    for keyF in keysInFelony:
                        zipCode = keyF
                        felonyNumber = felonyAccumulation.pop(keyF)
                        if keyF in misdemeanorAccumulation:
                            misdemeanorNumber = misdemeanorAccumulation.pop(keyF)
                        else:
                            misdemeanorNumber = 0
                        if keyF in violationAccumulation:
                            violationNumber = violationAccumulation.pop(keyF)
                        else:
                            violationNumber = 0
                        outPutCSV.writerow([previousDateEntry,zipCode,felonyNumber,misdemeanorNumber,violationNumber])
                    #there may still be some zipcodes in misdemeanor and violation that were not a part of the felony zipcodes
                    keysInMisdemeanor = list(misdemeanorAccumulation.keys())
                    for keyD in keysInMisdemeanor:
                        zipCode = keyD
                        felonyNumber = 0
                        misdemeanorNumber = misdemeanorAccumulation.pop(keyD)
                        if keyD in violationAccumulation:
                            violationNumber = violationAccumulation.pop(keyD)
                        else:
                            violationNumber = 0
                        outPutCSV.writerow([previousDateEntry, zipCode, felonyNumber, misdemeanorNumber,violationNumber])
                    #there may still be zome zipcodes in violation that were not a part of the previous two
                    keysInViolation = list(violationAccumulation.keys())
                    for keyV in keysInViolation:
                        zipCode = keyV
                        felonyNumber = 0
                        misdemeanorNumber = 0
                        violationNumber = violationAccumulation.pop(keyV)
                        outPutCSV.writerow([previousDateEntry, zipCode, felonyNumber, misdemeanorNumber, violationNumber])
                    #clear all dictionaries, however they should all be empty at this point
                    felonyAccumulation.clear()
                    misdemeanorAccumulation.clear()
                    violationAccumulation.clear()
                #add our data into the accumulated dictionaries based on law_cat_id
                if row['law_cat_cd'] == "FELONY":
                    if row['zipcode'] in felonyAccumulation:
                        felonyAccumulation[row['zipcode']] += 1
                    else:
                        felonyAccumulation[row['zipcode']] = 1
                elif row['law_cat_cd'] == "MISDEMEANOR":
                    if row['zipcode'] in misdemeanorAccumulation:
                        misdemeanorAccumulation[row['zipcode']] += 1
                    else:
                        misdemeanorAccumulation[row['zipcode']] = 1
                elif row['law_cat_cd'] == "VIOLATION":
                    if row['zipcode'] in violationAccumulation:
                        violationAccumulation[row['zipcode']] += 1
                    else:
                        violationAccumulation[row['zipcode']] = 1
                previousDateEntry = currentDateEntry
            #need to write the last set of month into output
            keysInFelony = list(felonyAccumulation.keys())
            for keyF in keysInFelony:
                zipCode = keyF
                felonyNumber = felonyAccumulation.pop(keyF)
                if keyF in misdemeanorAccumulation:
                    misdemeanorNumber = misdemeanorAccumulation.pop(keyF)
                else:
                    misdemeanorNumber = 0
                if keyF in violationAccumulation:
                    violationNumber = violationAccumulation.pop(keyF)
                else:
                    violationNumber = 0
                outPutCSV.writerow([previousDateEntry,zipCode,felonyNumber,misdemeanorNumber,violationNumber])
            #there may still be some zipcodes in misdemeanor and violation that were not a part of the felony zipcodes
            keysInMisdemeanor = list(misdemeanorAccumulation.keys())
            for keyD in keysInMisdemeanor:
                zipCode = keyD
                felonyNumber = 0
                misdemeanorNumber = misdemeanorAccumulation.pop(keyD)
                if keyD in violationAccumulation:
                    violationNumber = violationAccumulation.pop(keyD)
                else:
                    violationNumber = 0
                outPutCSV.writerow([previousDateEntry, zipCode, felonyNumber, misdemeanorNumber,violationNumber])
            #there may still be zome zipcodes in violation that were not a part of the previous two
            keysInViolation = list(violationAccumulation.keys())
            for keyV in keysInViolation:
                zipCode = keyV
                felonyNumber = 0
                misdemeanorNumber = 0
                violationNumber = violationAccumulation.pop(keyV)
                outPutCSV.writerow([previousDateEntry, zipCode, felonyNumber, misdemeanorNumber, violationNumber])                    

            
            
                          
            
            
            
startTime = datetime.now()        
taxiDataAccumulator("C:/Users/Nishad/Desktop/Data/Cleaned/yellow_tripdata_2015-01Cleaned.csv","C:/Users/Nishad/Desktop/Data/Cleaned/Accumlated/yellow_tripdata_2015-01Accum.csv")
print(datetime.now() - startTime)        

            
    