# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:54:35 2017

@author: Iden
"""
import sys
sys.path.append("D:\\Capstone Data\\ranking_measures-master")
import measures

import pandas
import matplotlib.pyplot as plt

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm



def encodeDate(date):
    year = int(date[-4:])
    month = int(date[0:2])
    
    return ((year - 2010) * 12) + month - 1



# date must be in the format MM/YYYY
# data is pandas from final_trainingdata.csv
def linReg(zipCode, date, data):
    year = int(date[-4:])
    month = int(date[0:2])
    
    if year > 2015:
        date = "12/2015"
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
    year = int(date[-4:])
    month = int(date[0:2])
    
    if year > 2015:
        date = "12/2015"
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



"""
def svmLin(zipCode, date, data):
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
    
    SVMmodel = svm.SVR(kernel='linear')
    #SVMmodel = SVR(kernel = 'linear', C = 1e3)
    SVMmodel.fit(train[columns], train[target])
    
    values = zipData.groupby("date").get_group(date)
    # Delete columns we don't need
    del values["Unnamed: 0"]
    del values["Unnamed: 0.1"]
    del values["date"]
    del values["price"]
    prediction = SVMmodel.predict(values)
    return prediction    
    
def getSVMAccuracy(zipCode, data):
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
    test = zipData.loc[~zipData.index.isin(train.index)]
    
    SVMmodel = svm.SVR(kernel = 'linear', C = 1e3)
    SVMmodel.fit(train[columns], train[target])
    
    predictions = SVMmodel.predict(test[columns])
    return measures.find_rankdcg(test[target], predictions)
"""



def getLRAccuracy(zipCode, data):
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
    
    test = zipData.loc[~zipData.index.isin(train.index)]
    
    # Train model on data
    LRmodel = LinearRegression()
    LRmodel.fit(train[columns], train[target])
    
    predictions = LRmodel.predict(test[columns])
    return measures.find_rankdcg(test[target], predictions)



def getRFAccuracy(zipCode, data):
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
    
    test = zipData.loc[~zipData.index.isin(train.index)]
    
    # Train model on data
    RFmodel = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)
    RFmodel.fit(train[columns], train[target])
    
    predictions = RFmodel.predict(test[columns])
    return measures.find_rankdcg(test[target], predictions)


def printLR(zipCode, data):
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
    
    test = zipData.loc[~zipData.index.isin(train.index)]
    
    # Train model on data
    LRmodel = LinearRegression()
    LRmodel.fit(train[columns], train[target])
    
    predictions = LRmodel.predict(test[columns])
    
    plt.plot_date(test["date"], predictions, label = "Model")
    plt.plot_date(test["date"], test["price"], label = "Data")
    plt.legend()
    plt.show()
    

# Read data
data = pandas.read_csv("D:\\Capstone Data\\final_trainingdata.csv")

# Get all unique ZIP codes
zips = data.zipcode.unique()

measure = []

for z in zips:
    measure.append(getLRAccuracy(z, data))
    printLR(z, data)
    # measure.append(getRFAccuracy(z, data))
    # measure.append(getSVMAccuracy(z, data))
    
total = 0
for i in range(0, len(measure)):
    total += measure[i]
    print(zips[i], ":  ", measure[i])
    
print("Average accuracy: ", total/len(measure))
    
"""
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

"""
"""
zipCode = 10001
date = "12/2015"
shape = futureReg(zipCode, data)
pred1 = futureLinReg(zipCode, date, shape, data)
pred2 = futureRandForest(zipCode, date, shape, data)
pred3 = linReg(zipCode, date, data)
pred4 = randomForest(zipCode, date, data)
pred5 = svmLin(zipCode, date, data)

print(pred1)
print(pred2)
print(pred3)
print(pred4)
print(pred5)
"""


"""
# Start Linear Regression
# Initialize the model class
model = LinearRegression()

# Fit the model to the training data
model.fit(train[columns], train[target])

# Generate predictions for the test set
predictions = model.predict(test[columns])

# Compute error between test predictions and actual values
print("MEAN SQUARED ERROR (LR): ", mean_squared_error(predictions, test[target]))

print("LR COEFFICIENTS: ", model.coef_)

print("ACTUAL PRICE")
plt.hist(data["price"])
plt.show()

print("LR PRICE")
plt.hist(predictions)
plt.show()

# End Linear Regression
"""
"""
# Start Random Forest

# Initialize the model with some parameters
model = RandomForestRegressor(n_estimators=100, min_samples_leaf=10, random_state=1)

# Fit model to data
model.fit(train[columns], train[target])

# Make predictions
predictions = model.predict(test[columns])

# Compute error
print("MEAN SQUARED ERROR (RF): ", mean_squared_error(predictions, test[target]))

print("ACTUAL PRICE")
plt.hist(data["price"])
plt.show()

print("RF PRICE")
plt.hist(predictions)
plt.show()

# End Random Forest
"""
