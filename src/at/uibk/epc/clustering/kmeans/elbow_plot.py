import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn import metrics
import os
from pathlib import Path

# https://towardsdatascience.com/clustering-with-k-means-1e07a8bfb7ca


def calculate_metrics(slim_data_df, nr_clusters, country):
    # The next step is to scale our values to give them all equal importance.
    # Scaling is also important from a clustering perspective as the distance between points affects the way clusters are formed.
    slim_fitted_df = StandardScaler().fit_transform(slim_data_df)

    # Set number of clusters at initialisation time
    k_means = KMeans(n_clusters=nr_clusters)
    # Run the clustering algorithm
    k_means.fit(slim_fitted_df)

    # Calculating the silhouette coefficient…
    labels = k_means.labels_
   # print(labels)
    print(country + ' metrics for ' + str(nr_clusters) + ' clusters:')
    print('Silhouette score ' +
          str(metrics.silhouette_score(slim_fitted_df, labels, metric='euclidean')))

    # …and the CH score
    print('Calinski Harabasz score ' +
          str(metrics.calinski_harabasz_score(slim_fitted_df, labels)))
    print()

# Calculate the optimal number of clusters using the elbow method.
# An elbow plot shows at what value of k,
# the distance between the mean of a cluster and the other data points in the cluster is at its lowest.
# Two values are of importance here — distortion and inertia.
# Distortion is the average of the euclidean squared distance from the centroid of the respective clusters.
# Inertia is the sum of squared distances of samples to their closest cluster centre.


def elbow_plot_fct(slim_fitted_df, country):
    # For each value of k,
    # we can initialise k_means and use inertia to identify the sum of squared distances of samples to the nearest cluster centre
    sum_of_squared_distances = []
    K = range(2, 11)
    for k in K:
        k_means = KMeans(n_clusters=k)
        k_means.fit(slim_fitted_df)
        sum_of_squared_distances.append(k_means.inertia_)

    # Remember we care about intra-cluster similarity in K-means and this is what an elbow plot helps to capture.
    plt.plot(K, sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('sum_of_squared_distances')
    plt.title(country+': elbow method for optimal k')

    here = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(Path(here).parent, 'plots',
                            'elbow_plots', country + '_elbow_plot.png')
    plt.savefig(filename)
