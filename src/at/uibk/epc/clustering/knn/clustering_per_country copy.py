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

# for data in englandData:
#    print(data.get('awardedRating').get('ratingLevel'))
#    break
# print(pd.DataFrame(englandData).describe())

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.describe().transpose())
print(data_df.head())

print("size of data_df")
print(data_df.size)
print("the last element")
print(data_df.last)
print("size of data_df after calling last")
print(data_df.size)

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

# comparing the error rate with the k value
error = []

# Calculating error for K values between 1 and 40
# In each iteration the mean error for predicted values of test set is calculated and the result is appended to the error list.
for i in range(1, 40):
    knn = KNeighborsClassifier(n_neighbors=i, metric='manhattan')
    knn.fit(X_train, y_train)
    pred_i = knn.predict(X_test)
    error.append(np.mean(pred_i != y_test))

# The next step is to plot the error values against K values. Execute the following script to create the plot:
plt.figure(figsize=(12, 6))
plt.plot(range(1, 40), error, color='red', linestyle='dashed', marker='o',
         markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value')
plt.xlabel('K Value')
plt.ylabel('Mean Error')
plt.show()

# predict only one stuff
# single = np.array(
#    [['69', '1', '151', '22', '37', '0', '65', '140', '90', '2', '1', '0', '0']])
# prediction = model.predict(single)
# print(prediction)

# single = np.array(['69', '1', '151', '22', '37', '0', '65',
#                   '140', '90', '2', '1', '0', '0', '1'])
# singledf = pd.DataFrame(single)
# final = singledf.transpose()
# prediction = model.predict(final)
# print(prediction)
