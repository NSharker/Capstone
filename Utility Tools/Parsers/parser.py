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



        

complaintDataParser("NYPD_Complaint_Data_Historic.csv","output.csv")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #with open(outputFileName, 'wb') as writecsvfile:
         #   writer = csv.writer(writecsvfile)
          #  for row in complaintData:
            