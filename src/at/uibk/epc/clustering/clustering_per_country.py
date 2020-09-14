from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawDataEngland


englandData = getRawDataEngland()

# for data in englandData:
#    print(data.get('awardedRating').get('ratingLevel'))
#    break
# print(pd.DataFrame(englandData).describe())

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.describe().transpose())

# https://datatofish.com/k-means-clustering-python/
slim_data_df = pd.DataFrame(
    data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])

# fitting the data is quite important, the clusters are now more like circles; the non-fitted data was more like strapes.
slim_fitted_df = StandardScaler().fit_transform(slim_data_df)

# kmeans = KMeans(n_clusters=7, init='k-means++').fit(slim_data_df)
# what about fir_predict?
kmeans = KMeans(n_clusters=7, init='k-means++').fit(slim_fitted_df)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
print(centroids)
print(labels)

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


# append a new column cluster number to the original data
data_df['cluster_number'] = labels
print('original data and the corresponfing cluster numbers')
print(data_df.head())

# display the rating level from the original data and the clister number form the fitted data
rating_vs_cluster_data_df = pd.DataFrame(
    data_df, columns=['awardedRating_ratingLevel', 'cluster_number'])
print(rating_vs_cluster_data_df)

# print(slim_fitted_df[:, 0])  # all rows, 0 column
# print(slim_fitted_df[:, 1])  # all rows, 1 column

# plt.scatter(slim_data_df['ratedDwelling_spatialData_totalFloorArea_value'],
#            slim_data_df['ratedDwelling_thermalData_finalEnergyDemand_value'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)

plt.scatter(slim_fitted_df[:, 0],
            slim_fitted_df[:, 1], c=kmeans.labels_.astype(float), s=50, alpha=0.5)


plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()