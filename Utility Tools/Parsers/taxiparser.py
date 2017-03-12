# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
from geopy.distance import great_circle
from datetime import datetime

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

"""
def calcCorrect(inputFileName1, inputFileName2):
    with open(inputFileName1, 'r') as testFile:
        with open(inputFileName2, 'r') as checkFile:
            testData = csv.DictReader(testFile, delimiter = ',')
            checkData = csv.DictReader(checkFile, delimiter = ',')
            testPick = []
            testDrop = []
            checkPick = []
            checkDrop = []
            for row in testData:
                pickZip = int(row['pickup_zip'])
                dropZip = int(row['dropoff_zip'])
                testPick.append(pickZip)
                testDrop.append(dropZip)
            for row in checkData:
                pickCheckZip = int(row['pickup_zip'])
                dropCheckZip = int(row['dropoff_zip'])
                checkPick.append(pickCheckZip)
                checkDrop.append(dropCheckZip)
            total = 40
            correct = 0
            for i in range(0, 20):
                if testPick[i] == checkPick[i]:
                    correct += 1
                if testDrop[i] == checkDrop[i]:
                    correct += 1
            print("Correct: ", correct/total)
"""

# startTime = datetime.now()
# nyZipDict = getZipDict("")
# taxiDataParser("", "", nyZipDict)
# print(datetime.now() - startTime)