import pickle
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
country = 'England'

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.describe().transpose())
print(data_df.head())

print("nr. of elements considered: ")
print(len(data_df.index))

# https://datatofish.com/k-means-clustering-python/
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

# Training and Predictions
classifier = KNeighborsClassifier(n_neighbors=15, metric='manhattan')
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

# evaluating the algorithm
# For evaluating an algorithm, confusion matrix, precision, recall and f1 score are the most commonly used metrics.
# The confusion_matrix and classification_report methods of the sklearn.metrics can be used to calculate these metrics.
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# pickle - save model to file
filename = "serialized_pickle_model_england.pck"

here = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(here, 'persisted_models/'+filename)

with open(filepath, 'wb') as f:
    pickle.dump(classifier, f)

# pickle - load model from file
loaded_model = pickle.load(open(filepath, 'rb'))
result_load = loaded_model.score(X_test, y_test)
print("accuracy score from loaded model")
print(result_load)

Ypredict_from_load = loaded_model.predict(X_test)
print("prediction on X_test")
print(Ypredict_from_load)

#new_data_rows = [[481, 127], [23, 325], [52, 284], [387, 381]]
new_data_rows = [[387, 381]]
#new_data_rows = [[481, 127]]
new_data_df = pd.DataFrame(
    new_data_rows, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])
print(new_data_df.head())

#new_data_label = ['C', 'C', 'D', 'D']
new_data_label = ['D']
#new_data_label = ['C']
new_label_df = pd.DataFrame(
    new_data_label, columns=['awardedRating_ratingLevel'])
print(new_label_df.head())

new_X = new_data_df
new_y = new_label_df.values.ravel()

print("the dwelling that should be rated is:")
print(new_X)
print(new_y)

new_X = scaler.transform(new_X)

new_pred = classifier.predict(new_X)
print("new prediction")
print(new_pred)

print("results")
print(confusion_matrix(new_y, new_pred))
print(classification_report(new_y, new_pred))

print("prediction for on element by the loaded_model")
loaded_predict = loaded_model.predict(new_X)
print(loaded_predict)

print("results for loaded model")
print(confusion_matrix(new_y, loaded_predict))
print(classification_report(new_y, loaded_predict))

# how to find out the k nearest neighbours
# https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html

# doesn't really work :(
# neighter with the 15 or 3 neighbors
nr_of_neighbors = 5
neighbors = classifier.kneighbors(X=new_X, n_neighbors=nr_of_neighbors)
print("The closest neighbors are ([distance, row_index])")
print(neighbors)

for i in range(0, nr_of_neighbors):
    # the id of the neighboars: neighbors[1][0][i]
    print(data_df.iloc[neighbors[1][0][i], :])

# sort by distance
# get the first n elements, as the first n closest neighbors
#outputlist = sorted(neighbors[0], key=itemgetter(0))
#print("sorted array")
# print(outputlist)

# the radius neighbors
# https: // scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html
classifier_radius = RadiusNeighborsClassifier(radius=5)
classifier_radius.fit(X_train, y_train)
y_pred_radius = classifier_radius.predict(X_test)

print("radius prediction")
print(y_pred_radius)

print("Accuracy radius classifier")
print(confusion_matrix(y_test, y_pred_radius))
print(classification_report(y_test, y_pred_radius))

y_pred_radius_for_one = classifier_radius.predict(new_X)

print("radius prediction for one")
print(y_pred_radius_for_one)

print("Accuracy radius classifier for one")
print(confusion_matrix(new_y, y_pred_radius_for_one))
print(classification_report(new_y, y_pred_radius_for_one))

radius_neighbors = classifier_radius.radius_neighbors(X=new_X, return_distance=True,
                                                      sort_results=True)

print("radius neighbors")
print("The closest neighbors are ([distance, row_index])")
print(radius_neighbors)

for i in range(0, nr_of_neighbors):
    # the id of the neighboars: neighbors[1][0][i]
    print(data_df.iloc[radius_neighbors[1][0][i], :])

# graph = classifier.kneighbors_graph(
#   X=new_X, n_neighbors=nr_of_neighbors, mode='distance')
# How to plot the graph?
#plt.figure(figsize=(12, 6))
#plt.plot(graph.toarray(), new_X, color='red', linestyle='dashed', marker='o',)
#plt.title('Closest neighbors')
#plt.xlabel('K Value')
#plt.ylabel('Mean Error')
# plt.show()

# https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/
# save and load trained models
