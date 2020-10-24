import joblib
from sklearn.neighbors import RadiusNeighborsClassifier
from operator import itemgetter
import operator
from sklearn.model_selection import GridSearchCV
from pathlib import Path
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawDataEngland
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

englandData = getRawDataEngland()
country = ('England').lower()

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.describe().transpose())
print(data_df.head())

print("nr. of elements considered: ")
print(len(data_df.index))

# save dataframe to file for later use, for the api
filenameRadiusDf = "serialized_radius_dataframe_" + country + ".pck"

here = os.path.dirname(os.path.abspath(__file__))
filepathDf = os.path.join(
    here, 'persisted_models', country, filenameRadiusDf)
joblib.dump(data_df, filepathDf)

# triming down the dataframe
slim_data_df = pd.DataFrame(
    data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])
print(slim_data_df.head())
labels_df = pd.DataFrame(
    data_df, columns=['awardedRating_ratingLevel'])
print(labels_df.head())

X = slim_data_df
y = labels_df.values.ravel()

# split the data in test and train data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
print("split done")


# fitting the data is quite important
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# saving scaler for later use
scalerFilename = "serialized_radius_scaler_" + country + ".pck"

here = os.path.dirname(os.path.abspath(__file__))
filepathScaler = os.path.join(
    here, 'persisted_models', country, scalerFilename)
joblib.dump(scaler, filepathScaler)

# load data from file
#print("loading data  from file")
#here = os.path.dirname(os.path.abspath(__file__))

#filename = "serialized_X_train_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#X_train = joblib.load(filepath)

#filename = "serialized_X_test_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#X_test = joblib.load(filepath)

#filename = "serialized_y_train_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#y_train = joblib.load(filepath)

#filename = "serialized_y_test_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#y_test = joblib.load(filepath)

#print("loading data finished")

# the radius neighbors
# https: // scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html

classifier_radius = RadiusNeighborsClassifier(
    radius=5, metric='euclidean', weights='distance')
classifier_radius.set_params(outlier_label='Z')
classifier_radius.fit(X_train, y_train)
y_pred_radius = classifier_radius.predict(X_test)

print("radius prediction")
print(y_pred_radius)

print("Accuracy radius classifier")
print(confusion_matrix(y_test, y_pred_radius))
print(classification_report(y_test, y_pred_radius))

# joblib - save model to file
filenameRadiusClassifier = "serialized_radius_classifier_" + country + ".pck"

here = os.path.dirname(os.path.abspath(__file__))
filepathRadiusClassifier = os.path.join(
    here, 'persisted_models', country, filenameRadiusClassifier)
joblib.dump(classifier_radius, filepathRadiusClassifier)
