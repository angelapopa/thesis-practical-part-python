# https://stackabuse.com/k-nearest-neighbors-algorithm-in-python-and-scikit-learn/

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# importing the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# Assign colum names to the dataset
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']

# Read dataset to pandas dataframe
dataset = pd.read_csv(url, names=names)

print(dataset.head())


# Preprocessing
# split our dataset into its attributes and labels.
# The X variable contains the first four columns of the dataset(i.e. attributes) while y contains the labels.
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

# split the data in test and train data
# To avoid over-fitting, we will divide our dataset into training and test splits,
# which gives us a better idea as to how our algorithm performed during the testing phase.
# This way our algorithm is tested on un-seen data, as it would be in a production application.
# The following method call splits the dataset into 80% train data and 20% test data.
# This means that out of total 150 records, the training set will contain 120 records and the test set contains 30 of those records.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Feature Scaling
# Before making any actual predictions, it is always a good practice to scale the features so that all of them can be uniformly evaluated.
scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Training and Predictions
# There is no ideal value for K and it is selected after testing and evaluation,
# however to start out, 5 seems to be the most commonly used value for KNN algorithm.
classifier = KNeighborsClassifier(n_neighbors=5)
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
    knn = KNeighborsClassifier(n_neighbors=i)
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
