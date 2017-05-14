import numpy as np

from sklearn import preprocessing
from sklearn import linear_model
from pymongo import MongoClient
from . import mongoquerytrainingdata as mqt

# TODO:
# Make test/training set for statistical analysis




# Dunno where i should put this. One of last steps for data preperation.
"""

# Label Encoder
le = preprocessing.LabelEncoder()
# Create mappings for sorted datews
le.fit(final["date"])

# Using the mapping make a new column with integer encoding of chronological dates
final["date_enc"] = le.transform(final["date"])
# Drop all rows with any NaN valyes
final_nan = final.dropna()
final_nan.to_csv("final_trainingdata.csv")

"""



# TODO: Allow past dates?
# Encode a date
def encodeFuture(month, year):
	# Error checking
	if (year <= 2010 or month < 1 or month > 12):
		return -1
	return ((year - 2010) * 12) + month - 1

# Create all regressions for a zip code
# Queries mongo for zipcode
def formulateZipcodeRegressions(zipcode):
	result = mqt.query_trainingdata( {"zipcode":zipcode} )
	# If no result from query back out
	if (result == None):
		print("ZipcodeNotFound")
		return None

	returnVal = {}
	# All the regressions we would need
	returnVal["prices_reg"] = linear_model.LinearRegression()
	returnVal["pickup_reg"] = linear_model.LinearRegression()
	returnVal["pickup_pass_reg"] = linear_model.LinearRegression()
	returnVal["dropoff_reg"] = linear_model.LinearRegression()
	returnVal["dropoff_pass_reg"] = linear_model.LinearRegression()
	returnVal["felonies_reg"] = linear_model.LinearRegression()
	returnVal["misdemeanors_reg"] = linear_model.LinearRegression()
	returnVal["violations_reg"] = linear_model.LinearRegression()

	# Init buckets
	features = []
	pickups = []
	pickups_pass = []
	dropoffs = []
	dropoffs_pass = []
	felonies = []
	misdemeanors = []
	violations = []
	prices = []
	date_enc = []
	# Features Format: [date_enc, pickups, dropoffs, pickups_passengers, dropoffs_passengers, felonies, misdemeanors, violations]
	# Collect values into appropriate buckets from queries
	for dic in result:
		features_cell = []
		
		pickups.append(dic["pickups"])
		dropoffs.append(dic["dropoffs"])
		pickups_pass.append(dic["pickup_passengers"])
		dropoffs_pass.append(dic["dropoff_passengers"])
		felonies.append(dic["FELONIES"])
		misdemeanors.append(dic["MISDEMEANORS"])
		violations.append(dic["VIOLATIONS"])
		prices.append(dic["price"])
		date_enc.append(dic["date_enc"])

		features_cell.append(dic["date_enc"])
		features_cell.append(dic["pickups"])
		features_cell.append(dic["dropoffs"])
		features_cell.append(dic["pickup_passengers"])
		features_cell.append(dic["dropoff_passengers"])
		features_cell.append(dic["FELONIES"])
		features_cell.append(dic["MISDEMEANORS"])
		features_cell.append(dic["VIOLATIONS"])

		features.append(features_cell)

	# Reshape the lists into nparrays to silence depreciation warnings
	features = np.array(features).reshape(len(features), len(features[0]))
	pickups = np.array(pickups).reshape(len(pickups), 1)
	pickups_pass = np.array(pickups_pass).reshape(len(pickups_pass), 1)
	dropoffs = np.array(dropoffs).reshape(len(dropoffs), 1)
	dropoffs_pass = np.array(dropoffs_pass).reshape(len(dropoffs_pass), 1)
	felonies = np.array(felonies).reshape(len(felonies), 1)
	misdemeanors = np.array(misdemeanors).reshape(len(misdemeanors), 1)
	violations = np.array(violations).reshape(len(violations), 1)
	prices = np.array(prices).reshape(len(prices), 1)
	date_enc = np.array(date_enc).reshape(len(date_enc), 1)

	# If lengths match up, fit x and y values for all regressions
	if (len(features) == len(prices)):
		returnVal["prices_reg"].fit(features, prices)
		returnVal["pickup_reg"].fit(date_enc, pickups)
		returnVal["pickup_pass_reg"].fit(date_enc, pickups_pass)
		returnVal["dropoff_reg"].fit(date_enc, dropoffs)
		returnVal["dropoff_pass_reg"].fit(date_enc, dropoffs_pass)
		returnVal["felonies_reg"].fit(date_enc, felonies)
		returnVal["misdemeanors_reg"].fit(date_enc, misdemeanors)
		returnVal["violations_reg"].fit(date_enc, violations)
	else:
		"SIZE_OF_FEATURES != SIZE_OF_VALUES"
	# Retrun the regressions
	return returnVal

# Predict a housing price for a given month and year based on data we have already
# Returns a list of the values for that month in the following format
# [date_enc, pickups, pickup_pass, dropoffs, dropoff_pass, felonies, misdemeanors, violations, price]
def predictHousingPrice(month, year, zipcode, pickups=None, pickup_pass=None, dropoffs=None, dropoffs_pass=None, felonies=None, misdemeanors=None, violations=None):
	# Get regressions
	zipcode_regressions = formulateZipcodeRegressions(zipcode)
	option = 1
	# If some error, back out
	if (zipcode_regressions == None):
		return None
	# Encode the future date
	query_reg = np.array([encodeFuture(month, year)]).reshape(-1,1)
	# Return the price prediction when using the projected values for the other Xs
	if (pickups==None and pickup_pass==None and dropoffs==None and dropoffs_pass==None and felonies==None and misdemeanors==None and violations==None):
		option = 0
		predict_input = [
				query_reg[0][0], 
				zipcode_regressions["pickup_reg"].predict(query_reg)[0][0],
				zipcode_regressions["pickup_pass_reg"].predict(query_reg)[0][0],
				zipcode_regressions["dropoff_reg"].predict(query_reg)[0][0],
				zipcode_regressions["dropoff_pass_reg"].predict(query_reg)[0][0],
				zipcode_regressions["felonies_reg"].predict(query_reg)[0][0],
				zipcode_regressions["misdemeanors_reg"].predict(query_reg)[0][0],
				zipcode_regressions["violations_reg"].predict(query_reg)[0][0]
		]
	else:
		predict_input = [
			query_reg[0][0], 
			pickups,
			pickup_pass,
			dropoffs,
			dropoffs_pass,
			felonies,
			misdemeanors,
			violations
		]
	predict_nd = np.array(predict_input).reshape(1,-1)
	priceVal = zipcode_regressions["prices_reg"].predict(predict_nd)[0][0]
	predict_input.append(priceVal)
	temp = {}
	temp['pickups'] = int(predict_input[1])
	temp['pickup_passengers'] = int(predict_input[2])
	temp['dropoffs'] = int(predict_input[3])
	temp['dropoff_passengers'] = int(predict_input[4])
	temp['FELONIES'] = int(predict_input[5])
	temp['MISDEMEANORS'] = int(predict_input[6])
	temp['VIOLATIONS'] = int(predict_input[7])
	temp['price'] = int(predict_input[8])
	return temp


