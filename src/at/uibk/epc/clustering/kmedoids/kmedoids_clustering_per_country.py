from db_data_per_country import getRawDataEngland
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# limit 40.000 is ok but takes a lot of time to process and cluster 3 is empty for k=5.
# limit 10.000, cluster=5, inertia aprox 5300
limit = 10000
clusters = 7
englandData = getRawDataEngland(limit)
country = 'England'

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.describe().transpose())

# https://datatofish.com/k-means-clustering-python/
slim_data_df = pd.DataFrame(
    data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])

print(slim_data_df.head)

# fitting the data is quite important, the clusters are now more like circles; the non-fitted data was more like strapes.
slim_fitted_df = StandardScaler().fit_transform(slim_data_df)

# preset the number of clusters
kmedoids = KMedoids(n_clusters=clusters, random_state=0).fit(slim_fitted_df)
print("labels")
print(kmedoids.labels_)

# Displays the cluster centers, here called medoids, which are points from the original dataset
print("Cluster centers")
print(kmedoids.cluster_centers_)

print("inertia")
print(kmedoids.inertia_)

print("predictions")
print(kmedoids.predict([[-0.98965, -0.3211], [0.6, -0.300]]))

plt.scatter(slim_fitted_df[:, 0],
            slim_fitted_df[:, 1], c=kmedoids.labels_.astype(float), s=50, alpha=0.5)

centroids = kmedoids.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)

here = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(Path(here).parent, 'plots',
                        'kmedoid_plots', country + '_kmedoid_plot.png')
plt.savefig(filename)

# function that creates a dataframe for cluster centers with a column for cluster number


def pd_centers(cols_of_interest, centers):
    colNames = list(cols_of_interest)
    colNames.append('cluster_number')
    # Zip with a column called 'prediction' (index)
    Z = [np.append(A, index) for index, A in enumerate(centers)]
    # Convert to pandas data frame for plotting
    P = pd.DataFrame(Z, columns=colNames)
    P['cluster_number'] = P['cluster_number'].astype(int)
    return P


P = pd_centers(['ratedDwelling_spatialData_totalFloorArea_value',
                'ratedDwelling_thermalData_finalEnergyDemand_value'], centroids)
print('Centroids (x,y,label) for the fitted data')
print(P)

# we have the array with labels (cluster numbers)
# so we add a new column with cluster numbers to the original data
labels = kmedoids.labels_
data_df['cluster_number'] = labels
print('original data and the corresponfing cluster numbers')
print(data_df)

# display the rating level from the original data and the cluster number form the fitted data
rating_vs_cluster_data_df = pd.DataFrame(
    data_df, columns=['awardedRating_ratingLevel', 'cluster_number'])
print(rating_vs_cluster_data_df)

# group by rating level
print(rating_vs_cluster_data_df.groupby(
    ["awardedRating_ratingLevel", "cluster_number"])['cluster_number'].count())

# => there is no clear relation btw. rating_level and cluster number
