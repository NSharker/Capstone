

from sklearn import preprocessing
from sklearn import linear_model

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



