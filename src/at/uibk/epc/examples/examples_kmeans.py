# importing required libraries
from sklearn.preprocessing import StandardScaler
import os
from sklearn import cluster, datasets
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline


# example from https://www.toptal.com/machine-learning/clustering-algorithms
# updates to current API by following https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html#sklearn.datasets.load_iris
iris = datasets.load_iris()
Xiris = iris.data
yiris = iris.target

kmeans = cluster.KMeans(n_clusters=3)
kmeans.fit(Xiris)

print("The IRIS dataset, toptal example")
print(kmeans.labels_[::10])
print(yiris[::10])

# example https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html#sklearn.datasets.load_iris
print("The IRIS dataset, scikit-learn example")
print(iris.target[[10, 25, 50]])
print(list(iris.target_names))

# example from https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-k-means-clustering/
print("The wholesale customer segmentation example")

# reading the data and looking at the first five rows of the data
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'Wholesale_customers_data.csv')
data = pd.read_csv(filename)

# print the first rows
print("original data")
print(data.head())

# statistics of the data
print("statistics on the original data")
print(data.describe())

# some columns in the dataset are of high magnitude (449, 6583) and some are low magnitude (2, 3, etc.)
# K-Means is a distance-based algorithm, this difference of magnitude can create a problem,
# so we need to standardize the data and bring it to the same magnitude

# standardizing the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

print("scaled data")
print(data_scaled[:5, :8])  # first 5 rows, and 3 columns

# statistics of scaled data
print("statistics on the scaled data")
print(pd.DataFrame(data_scaled).describe())

# defining the kmeans function with initialization as k-means++
kmeans = KMeans(n_clusters=2, init='k-means++')

# fitting the k means algorithm on scaled data
kmeans.fit(data_scaled)

# evaluate how well formed the cluster are
print("Inertia ")
print(kmeans.inertia_)

# We will first fit multiple k - means models and in each successive model, we will increase the number of clusters.
# #We will store the inertia value of each model and then plot it to visualize the result

# fitting multiple k-means algorithms and storing the values in a list
SSE = []
for cluster in range(1, 20):
    kmeans = KMeans(n_clusters=cluster, init='k-means++')
    kmeans.fit(data_scaled)
    SSE.append(kmeans.inertia_)

# converting the results into a dataframe and plotting them
frame = pd.DataFrame({'Cluster': range(1, 20), 'SSE': SSE})
plt.figure(figsize=(12, 6))
plt.plot(frame['Cluster'], frame['SSE'], marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')

# plt.show()

# based on the plot it is visible that we can choose any number of clusters between 5 to 8.
# k means using 5 clusters and k-means++ initialization
kmeans = KMeans(n_clusters=5, init='k-means++')
kmeans.fit(data_scaled)
pred = kmeans.predict(data_scaled)

# Finally, let’s look at how many data points are in each of the above-formed clusters
frame = pd.DataFrame(data_scaled)
frame['cluster'] = pred

print("Number of data points in each cluster")
print(frame['cluster'].value_counts())
