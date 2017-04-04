# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 11:08:43 2017

@author: Iden
"""

import pandas as pd




def zillowParserHome(inputFileName, outputFileName):
    df = pd.read_csv(inputFileName, sep = ',')              
    left = df.iloc[:, (1, 3, 5)]                            # Select columns RegionName, State, and CountyName; store in data frame left
    right = df.iloc[:, range(172, 244)]                     # Select range of dates; store in data frame right
    result = left.join(right)                               # Join right and left data frames
    final = result.loc[result['State'] == 'NY']             # Filter for only entries in NY
                                                            # Filter for only counties in NYC
    final = final.loc[result['CountyName'].isin(['New York', 'Queens', 'Kings', 'Bronx', 'Richmond'])]
    del final['CountyName']                                 # Delete CountyName column
    del final['State']                                      # Delete State column
    final = final.rename(columns={'RegionName': 'zipcode'})
    final.to_csv(outputFileName, index = False)             # Write clean data frame to file
    print("Done")
    
def zillowParserRental(inputFileName, outputFileName):
    df = pd.read_csv(inputFileName, sep = ',')
    rows, columns = df.shape
    #left = df.iloc[:, (0, 2, 4)]                            # Select columns RegionName, State, and CountyName, store in data frame left
    left = df.iloc[:, (1, 3, 5)]                            # Columns for Zip_ZriPerSqft_AllHomes.csv
    #right = df.iloc[:, range(6, columns-14)]                # Select columns 7 to number of columns - 14
    right = df.iloc[:, range(7, columns-14)]                # Column range for Zip_ZriPerSqft_AllHomes.csv
    result = left.join(right)                               # Join right and left data frames
    final = result.loc[result['State'] == 'NY']             # Filter for only entries in NY
                                                            # Filter for only entries in NYC
    final = final.loc[result['CountyName'].isin(['New York', 'Queens', 'Kings', 'Bronx', 'Richmond'])]
    del final['CountyName']                                 # Delete CountyName column
    del final['State']                                      # Delete State column
    final = final.rename(columns={'RegionName': 'zipcode'})
    final.to_csv(outputFileName, index = False)             # Write clean data frame to file
    print("Done")
    

    
    
inputFileName = "--INPUT-FILE-NAME--"
outputFileName = "--OUTPUT-FILE-NAME--"
# zillowParserHome(inputFileName, outputFileName)
zillowParserRental(inputFileName, outputFileName)