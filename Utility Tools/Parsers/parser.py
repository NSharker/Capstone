# -*- coding: utf-8 -*-
"""

@author: Nishad
"""
import csv

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

        

#complaintDataParser("NYPD_Complaint_Data_Historic.csv","output.csv")


taxiDataParser("yellow_tripdata_2010-01.csv", "yellow2010output.csv")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #with open(outputFileName, 'wb') as writecsvfile:
         #   writer = csv.writer(writecsvfile)
          #  for row in complaintData:
            