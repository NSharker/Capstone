

from sklearn import preprocessing
from sklearn import linear_model

# Label Encoder
le = preprocessing.LabelEncoder()
# Create mappings for sorted datews
le.fit(final["date"])

# Using the mapping make a new column with integer encoding of chronological dates
final["date_enc"] = le.transform(final["date"])
# Drop all rows with any NaN valyes
final_nan = final.dropna()




# Init Linear regression
reg = linear_model.LinearRegression()

# How fit works:
# reg.fit(features, value_to_predict)
reg.fit( [final_nan["date_enc"], final_nan["zipcode"], final_nan["pickups"], final_nan["dropoffs"], final_nan["FELONIES"], final_nan["MISDEMEANORS"], final_nan["VIOLATIONS"]], final_nan["price"] )





# Above is good

# Below is Scratch 
features = pd.read_csv("final_trainingdata.csv")
values = pd.read_csv("final_trainingdata.csv")

# TODO: Figure out how to copy columns between dataframes
# Maybe just read the file again and drop the columns
del features["date"]
del features["pickup_passengers"]
del features["dropoff_passengers"]


final_nan.drop(final_nan.columns[[0, 1, 3]], axis=1, inplace=True)


features = pd.read_csv("final_trainingdata.csv")
values = pd.read_csv("final_trainingdata.csv")


features["date_enc"] = final_nan["date_enc"].astype(int)
features["zipcode"] = final_nan["zipcode"].astype(int)
features["pickups"] = final_nan["pickups"].astype(int)
features["dropoffs"] = final_nan["dropoffs"].astype(int)
features["FELONIES"] = final_nan["FELONIES"].astype(int)
features["MISDEMEANORS"] = final_nan["MISDEMEANORS"].astype(int)
features["VIOLATIONS"] = final_nan["VIOLATIONS"].astype(int)


values["price"]= final_nan["price"]

final_nan["zipcode"], final_nan["pickups"], final_nan["dropoffs"], final_nan["FELONIES"], final_nan["MISDEMEANORS"], final_nan["VIOLATIONS"]], final_nan["price"] )