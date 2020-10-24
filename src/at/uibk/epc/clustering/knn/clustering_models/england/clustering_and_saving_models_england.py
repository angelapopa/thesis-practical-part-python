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
scalerFilename = "serialized_scaler_" + country + ".pck"

here = os.path.dirname(os.path.abspath(__file__))
filepathScaler = os.path.join(
    here, 'persisted_models', country, scalerFilename)
joblib.dump(scaler, filepathScaler)

# saving train and test data for later use, for the radius classifier
#here = os.path.dirname(os.path.abspath(__file__))

#filename = "serialized_X_train_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#joblib.dump(X_train, filepath)

#filename = "serialized_X_test_" + country + ".pck"
# filepath = os.path.join(
#   here, 'persisted_models', country, filename)
#joblib.dump(X_test, filepath)

#filename = "serialized_y_train_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#joblib.dump(y_train, filepath)

#filename = "serialized_y_test_" + country + ".pck"
# filepath = os.path.join(
#    here, 'persisted_models', country, filename)
#joblib.dump(y_test, filepath)


# Training and Predictions
kNeighborsClassifier = KNeighborsClassifier(n_neighbors=15, metric='manhattan')
kNeighborsClassifier.fit(X_train, y_train)

y_pred = kNeighborsClassifier.predict(X_test)

print("kneighbors prediction")
print(y_pred)

# evaluating the algorithm
# For evaluating an algorithm, confusion matrix, precision, recall and f1 score are the most commonly used metrics.
# The confusion_matrix and classification_report methods of the sklearn.metrics can be used to calculate these metrics.
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# joblib - save model to file
filenamekNeighborsClassifier = "serialized_kNeighbors_classifier_" + country + \
    ".pck"

here = os.path.dirname(os.path.abspath(__file__))
filepathkNeighborsClassifier = os.path.join(here, 'persisted_models',
                                            country, filenamekNeighborsClassifier)
# looks like dumping the model for ll the datasets in the db, predicts an 'F'
# dumping the model for 10000, predict a 'C'
joblib.dump(kNeighborsClassifier, filepathkNeighborsClassifier)
