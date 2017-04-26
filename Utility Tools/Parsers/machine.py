# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:54:35 2017

@author: Iden
"""

import pandas
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# Does not work - Need to fix
def futureReg(zipCode, iterations, data):
    grouped = data.groupby("zipcode")
    zipData = grouped.get_group(zipCode)
    columns = zipData.columns.tolist()
    
    values = zipData.groupby("date").get_group("12/2015")
    del values["Unnamed: 0"]
    del values["Unnamed: 0.1"]
    del values["date"]
    
    pCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "pickups"]]
    pTarget = "pickups"
    
    dCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "dropoffs"]]
    dTarget = "dropoffs"
    
    pPassCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "pickup_passengers"]]
    pPassTarget = "pickup_passengers"
    
    dPassCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "dropoff_passengers"]]
    dPassTarget = "dropoff_passengers"
    
    fCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "FELONIES"]]
    fTarget = "FELONIES"
    
    mCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "MISDEMEANORS"]]
    mTarget = "MISDEMEANORS"
    
    vCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "VIOLATIONS"]]
    vTarget = "VIOLATIONS"
    
    priceCol = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "price"]]
    priceTarget = "price"
    
    train = zipData.sample(frac = 0.8, random_state = 1)
    
    pModel = LinearRegression()
    pModel.fit(train[pCol], train[pTarget])
    pValues = values
    del pValues["pickups"]
    pPred = pModel.predict(pValues)
    print(pPred)
    
    dModel = LinearRegression()
    dModel.fit(train[dCol], train[dTarget])
    dValues = values
    del dValues["dropoffs"]
    dPred = dModel.predict(dValues)
    print(dPred)
    
    pPassModel = LinearRegression()
    pPassModel.fit(train[pPassCol], train[pPassTarget])
    pPassValues = values
    del pPassValues["pickup_passengers"]
    pPassPred = pPassModel.predict(pPassValues)
    print(pPassPred)
    
    dPassModel = LinearRegression()
    dPassModel.fit(train[dPassCol], train[dPassTarget])
    dPassValues = values
    del dPassValues["dropoff_passengers"]
    dPassPred = dPassModel.predict(dPassValues)
    print(dPassPred)
    
    fModel = LinearRegression()
    fModel.fit(train[fCol], train[fTarget])
    fValues = values
    del fValues["FELONIES"]
    fPred = fModel.predict(fValues)
    print(fPred)
    
    mModel = LinearRegression()
    mModel.fit(train[mCol], train[mTarget])
    mValues = values
    del mValues["MISDEMEANORS"]
    mPred = mModel.predict(mValues)
    print(mPred)
    
    vModel = LinearRegression()
    vModel.fit(train[vCol], train[vTarget])
    vValues = values
    del vValues["VIOLATIONS"]
    vPred = vModel.predict(vValues)
    print(vPred)
    
    priceModel = LinearRegression()
    priceModel.fit(train[priceCol], train[priceTarget])
    priceValues = values
    del priceValues["price"]
    pricePred = priceModel.predict(priceValues)
    print(pricePred)
    
    for i in range (0, (iterations - 1)):
        pPred1 = pModel.predict([dPred, pPassPred, dPassPred, fPred, mPred, vPred, pricePred])
        dPred1 = dModel.predict([pPred, pPassPred, dPassPred, fPred, mPred, vPred, pricePred])
        pPassPred1 = pPassModel.predict([pPred, dPred, dPassPred, fPred, mPred, vPred, pricePred])
        dPassPred1 = dPassModel.predict([pPred, dPred, pPassPred, fPred, mPred, vPred, pricePred])
        fPred1 = fModel.predict([pPred, dPred, pPassPred, dPassPred, mPred, vPred, pricePred])
        mPred1 = mModel.predict([pPred, dPred, pPassPred, dPassPred, fPred, vPred, pricePred])
        vPred1 = vModel.predict([pPred, dPred, pPassPred, dPassPred, fPred, mPred, pricePred])
        pricePred1 = priceModel.predict([pPred, dPred, pPassPred, dPassPred, fPred, mPred])
        
        pPred = pPred1
        dPred = dPred1
        pPassPred = pPassPred1
        dPassPred = dPassPred1
        fPred = fPred1
        mPred = mPred1
        vPred = vPred1
        pricePred = pricePred1
        
    return pricePred



# date must be in the format MM/YYYY
# data is pandas from final_trainingdata.csv
def linReg(zipCode, date, data):
    # Group data by zipcode
    grouped = data.groupby("zipcode")
    
    # Get data for only specific zipCode
    zipData = grouped.get_group(zipCode)
    
    # Get columns for training model
    columns = zipData.columns.tolist()
    columns = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "price"]]
    target = "price"
    
    # Take 80% of data for training, using random_state 1
    train = zipData.sample(frac = 0.8, random_state = 1)
    # test = zipData.loc[~zipData.index.isin(train.index)]
    
    # Train model on data
    LRmodel = LinearRegression()
    LRmodel.fit(train[columns], train[target])
    
    # Using specific date data from user, get a prediction from model and return it
    values = zipData.groupby("date").get_group(date)
    
    # Delete columns we don't need
    del values["Unnamed: 0"]
    del values["Unnamed: 0.1"]
    del values["date"]
    del values["price"]
    prediction = LRmodel.predict(values)
    return prediction

# date must be in the format MM/YYYY
# data is pandas from final_trainingdata.csv
def randomForest(zipCode, date, data):
    # Group data by zipcode
    grouped = data.groupby("zipcode")
    
    # Get data for only specific zipCode
    zipData = grouped.get_group(zipCode)
    
    # Get columns for training model
    columns = zipData.columns.tolist()
    columns = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "price"]]
    target = "price"
    
    # Take 80% of data for training, using random_state 1
    train = zipData.sample(frac = 0.8, random_state = 1)
    
    # Train model on data
    RFmodel = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    RFmodel.fit(train[columns], train[target])
    
    # Using specific date data from user, get a prediction from model and return it
    values = zipData.groupby("date").get_group(date)
    
    # Delete columns we don't need
    del values["Unnamed: 0"]
    del values["Unnamed: 0.1"]
    del values["date"]
    del values["price"]
    prediction = RFmodel.predict(values)
    return prediction



# Read data
data = pandas.read_csv("D:\\Capstone Data\\final_trainingdata.csv")

# Get user input
zipCode = input("Enter ZIP code: ")
zipCode = int(zipCode)
date = input("Enter date: ")

year = int(date[-4:])

# If user date is beyond our data, do a bunch of regressions 
if year > 2015:
    month = int(date[0:2])
    iterations = ((year - 2015 - 1) * 12) + month
    prediction = futureReg(zipCode, iterations, data)
    print("Linear Regression Future Prediction: ", prediction)
    
# Otherwise, just do a regression on what we've got
else:
    lr = linReg(zipCode, date, data)
    rf = randomForest(zipCode, date, data)
    print("Linear Regression Prediction: ", lr)
    print("Random Forest Prediction: ", rf)
    