

from sklearn import preprocessing
from sklearn import linear_model

import pandas
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

# TODO: Change LabelEncoding. Need to directly convert mo/year to number so that we can query future months
# Impliment predicting values
# Make code more modular


# Label Encoder
le = preprocessing.LabelEncoder()
# Create mappings for sorted datews
le.fit(final["date"])

# Using the mapping make a new column with integer encoding of chronological dates
final["date_enc"] = le.transform(final["date"])
# Drop all rows with any NaN valyes
final_nan = final.dropna()
final_nan.to_csv("final_trainingdata.csv")




# Init Linear regression
prices_reg = linear_model.LinearRegression()
pickup_reg = linear_model.LinearRegression()
dropoff_reg = linear_model.LinearRegression()
felonies_reg = linear_model.LinearRegression()
misdemeanors_reg = linear_model.LinearRegression()
violations_reg = linear_model.LinearRegression()

# How fit works:
# reg.fit(features, value_to_predict)
#reg.fit( [final_nan["date_enc"], final_nan["zipcode"], final_nan["pickups"], final_nan["dropoffs"], final_nan["FELONIES"], final_nan["MISDEMEANORS"], final_nan["VIOLATIONS"]], final_nan["price"] )





# Above is good

# Below is Scratch 
training_data = pd.read_csv("final_trainingdata.csv")
training_list = training_data.values.tolist() 
features = []
date_zipcode = []
pickups = []
dropoffs = []
felonies = []
misdemeanors = []
violations = []
prices = []
for row in training_list:
	features_cell = []
	date_zipcode_cell = []
	#
	features_cell.append(row[12])
	features_cell.append(row[3])
	date_zipcode_cell.append(row[12])
	date_zipcode_cell.append(row[3])
	#
	features_cell.append(row[4])
	pickups.append(row[4])
	#
	features_cell.append(row[5])
	dropoffs.append(row[5])
	#
	features_cell.append(row[8])
	felonies.append(row[8])
	#
	features_cell.append(row[9])
	misdemeanors.append(row[9])
	#
	features_cell.append(row[10])
	violations.append(row[10])
	#
	features.append(features_cell)
	date_zipcode.append(date_zipcode_cell)
	#
	prices.append(row[11])

if (len(features) == len(values)):
	pickup_reg.fit(date_zipcode, pickups)
	dropoff_reg.fit(date_zipcode, dropoffs)
	felonies_reg.fit(date_zipcode, felonies)
	misdemeanors_reg.fit(date_zipcode, misdemeanors)
	violations_reg.fit(date_zipcode, violations)
	prices_reg.fit(features, prices)
else:
	"SIZE_OF_FEATURES != SIZE_OF_VALUES"

# Iden's Machine Learning Stuff
# Random Forest is better than Linear Regression right now

data = pandas.read_csv("/Volumes/Big Stick/Capstone Data/final_trainingdata.csv")
# print(data.columns)
# print(data.shape)

# plt.hist(data["price"])
# plt.show()

# print(data.corr()["price"])
# Get all the columns from the dataframe
columns = data.columns.tolist()

# Filter the columns to remove ones we don't want
columns = [c for c in columns if c not in ["Unnamed: 0", "Unnamed: 0.1", "date", "price"]]

target = "price"


# Generate training set.  Set random state to be able to replicate results
train = data.sample(frac=0.8, random_state=1)

# Select anything not in the training set and put it in the testing set
test = data.loc[~data.index.isin(train.index)]

# Print shape
print(data.shape)
print(train.shape)
print(test.shape)

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

print("Linear Regression PRICE")
plt.hist(predictions)
plt.show()

# End Linear Regression
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

print("Random Forest PRICE")
plt.hist(predictions)
plt.show()

# End Random Forest

