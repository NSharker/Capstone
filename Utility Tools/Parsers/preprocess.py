
import rgtaxiparser
import accumulator
import os
import pandas as pd
from datetime import datetime

def timeAndRg(into, outo):
    startTime = datetime.now()
    rgtaxiparser.taxiDataParser(into, outo)
    print(datetime.now() - startTime)

def combineIntoOne(list_of_csvs):
    out_dataframe = pd.DataFrame()
    for x in list_of_csvs:
        df1 = pd.read_csv(x)
        out_dataframe = out_dataframe.append(df1, ignore_index=True)
    return out_dataframe

# This code assumes all of the taxi data is in folders
# by year and the original filenames were not changed



# The following generates the lists of files we are manipulating
####
inFiles = []
outFiles = []
accumFiles = []

startYear = 2010
endYear = 2015
startMonth = 1
endMonth = 12      
for x in range(startYear,endYear+1):
    for y in range(startMonth, endMonth+1):
        directory = str(x)
        if not os.path.exists(directory):
            os.makedirs(directory)
        inF = str(x)
        if (y > 9):
            inF = inF + "-"+str(y)
        else:
            inF = inF + "-0"+str(y)
        inFile = directory + "/" + inF +".csv"
        outFile = directory + "/" + "out/" + inF + ".csv"
        inFiles.append(directory + "/yellow_tripdata_" + inF +".csv")
        outFiles.append(directory + "/out/yellow_zip_" + inF +".csv")
        accumFiles.append(directory + "/out/yellow_accum_" + inF +".csv")
        if(x > 2012):
            if (x == 2013 and y < 8):
                s = 0
            else:
                inFiles.append(directory + "/green_tripdata_" + inF +".csv")
                outFiles.append(directory + "/out/green_zip_" + inF +".csv")
                accumFiles.append(directory + "/out/green_accum_" + inF +".csv")
#####

# For all inFiles, convert to zip code, outputs to corresponding file in outFiles
# NOTE: THIS DOES NOT WORK. RGTAXIPARSER MUST BE MANUALLY 
# CHANGED TO ACCOMODATE DIFFERENT HEADER NAMES
# TODO: Make this work dynamically
count = 0
for x in inFiles:
    timeAndRg(inFiles[count], outFiles[count])
    count = count + 1

# For all taxi files with zip codes, run accumulator for it output each to corresponding file
accumulator.batchTaxi(outFiles,accumFiles)

# Squish all of the accumulated files into one
data = combineIntoOne(accumFiles)

# We have yellow and green taxi data for many months. We want to combine by summing them
# This also sorts the rows by date and zipcode :)
data = data.groupby(["date", "zipcode"]).sum()

# The clean complaint file is expected to be in the folder this file is run from
# Second list is the intermediate results after sorting
# Third list is the final accumulated file
accumulator.batchComplaint(["NYPD_Complaint_Data_HistoricClean.csv"],["complaint_sorted.csv"],["complaint_accum.csv"])

# Read the accumulated   data
# We groupby and sum for all "date", "zipcode"
complaint = pd.read_csv("complaint_accum.csv")
complaint = complaint.groupby(["date", "zipcode"]).sum()

# Concatenate the complaint and taxi data
# TODO: Concatenate Pricing Data
all_data = pd.concat([data, complaint], axis=1)
data.to_csv("all_data.csv")








    


