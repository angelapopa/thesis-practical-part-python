from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path


def pd_centers(cols_of_interest, centers):
    colNames = list(cols_of_interest)
    colNames.append('cluster_number')
    # Zip with a column called 'prediction' (index)
    Z = [np.append(A, index) for index, A in enumerate(centers)]
    # Convert to pandas data frame for plotting
    P = pd.DataFrame(Z, columns=colNames)
    P['cluster_number'] = P['cluster_number'].astype(int)
    return P


def kmedoids_clustering(country, dbData, thermalFields, clusters, floor_area_outlier_borders, energy_consumption_outlier_borders):

    # https://hackersandslackers.com/json-into-pandas-dataframes/
    # json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
    data_df = pd.json_normalize(dbData, sep="_")
    print(data_df.describe().transpose())

    # https://datatofish.com/k-means-clustering-python/
    slim_data_df = pd.DataFrame(
        data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', thermalFields])

    print(slim_data_df.head)

    # fitting the data is quite important, the clusters are now more like circles; the non-fitted data was more like strapes.
    slim_fitted_df = StandardScaler().fit_transform(slim_data_df)

    # remove the outliers which we detected already visually by running a kmeans plot before
    print("=== Outliers")
    # however, first convert the data back into a dataframe
    slim_data_df_optimised = pd.DataFrame(
        slim_fitted_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', thermalFields])

    print(slim_data_df_optimised.shape)
    print(slim_data_df_optimised)

    print(country + ' outlier borders floor_area' +
          str(floor_area_outlier_borders))
    print(country + ' outlier borders energy_consumption' +
          str(energy_consumption_outlier_borders))

    print('Outliers')
    slim_data_df_optimised_floor_area = slim_data_df_optimised[slim_data_df_optimised[
        'ratedDwelling_spatialData_totalFloorArea_value'] >= floor_area_outlier_borders[0]]
    slim_data_df_optimised_energy_consumption = slim_data_df_optimised[
        slim_data_df_optimised[thermalFields] > energy_consumption_outlier_borders[0]]

    print(slim_data_df_optimised_floor_area)

    if country == 'England':
        slim_data_df_optimised_energy_consumption_lower = slim_data_df_optimised[
            slim_data_df_optimised[thermalFields] < energy_consumption_outlier_borders[1]]
        print(slim_data_df_optimised_energy_consumption_lower)
        frames = [slim_data_df_optimised_energy_consumption,
                  slim_data_df_optimised_energy_consumption_lower]
        slim_data_df_optimised_energy_consumption = pd.concat(
            frames, sort=False)
    print(slim_data_df_optimised_energy_consumption)

    print("Outliers indexes")
    index_outliers_floorArea = slim_data_df_optimised_floor_area.index.values
    index_outliers_thermal = slim_data_df_optimised_energy_consumption.index.values

    print("index_outliers_floorArea")
    print(index_outliers_floorArea)
    print("index_outliers_thermal")
    print(index_outliers_thermal)

    # Removing the Outliers
    slim_data_df_optimised = slim_data_df_optimised.drop(
        index=index_outliers_floorArea)
    slim_data_df_optimised = slim_data_df_optimised.drop(
        index=index_outliers_thermal)
    print("scaled data after droping the outliers")
    print(slim_data_df_optimised.shape)

    print("rechecking")
    print(slim_data_df_optimised[slim_data_df_optimised_floor_area])
    print(slim_data_df_optimised[slim_data_df_optimised_energy_consumption])

    print("transforming the optimised dataset back to an array")
    slim_data_df_optimised_as_array = slim_data_df_optimised.to_numpy()
    print(slim_data_df_optimised_as_array.shape)
    print(type(slim_data_df_optimised_as_array))

    # remove the same index rows in the original data
    data_df = data_df.drop(
        index=index_outliers_floorArea)
    data_df = data_df.drop(index=index_outliers_thermal)
    print("original data after droping the outliers")
    print(data_df.shape)

    print("=== Outliers END")

    # preset the number of clusters
    kmedoids = KMedoids(n_clusters=clusters,
                        random_state=0).fit(slim_data_df_optimised_as_array)
    print("labels")
    print(kmedoids.labels_)

    # Displays the cluster centers, here called medoids, which are points from the original dataset
    print("Cluster centers")
    print(kmedoids.cluster_centers_)

    print("inertia")
    print(kmedoids.inertia_)

    print("predictions")
    print(kmedoids.predict([[-0.98965, -0.3211], [0.6, -0.300]]))

    scatter = plt.scatter(slim_data_df_optimised_as_array[:, 0],
                          slim_data_df_optimised_as_array[:, 1], c=kmedoids.labels_.astype(float), s=50, alpha=0.5)

    centroids = kmedoids.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)

    plt.xlabel("floor area")
    plt.ylabel("energy consumption")

    plt.title(country + ":  " +
              str(len(slim_data_df_optimised_as_array) + 1) + " dwellings")

    plt.legend(*scatter.legend_elements(),
               loc='upper right', title="Clusters")

    here = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(Path(here).parent, 'plots',
                            'kmedoid_plots', country + '_kmedoid_plot.png')
    plt.savefig(filename)

    # function that creates a dataframe for cluster centers with a column for cluster number

    P = pd_centers(['ratedDwelling_spatialData_totalFloorArea_value',
                    thermalFields], centroids)
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
    return 'the END'
