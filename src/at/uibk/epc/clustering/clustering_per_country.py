from sklearn import metrics
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawDataEngland

englandData = getRawDataEngland()

# convert json to a matrix with 4 columns (id, floorArea, energyDemand, ratingLevel)
# python uses list of lists to represent a matrix
# dataFrameList = list()
# for d in dbData:
#    dataFrameList.append(d['awardedRating']['ratingLevel'])

# print(englandData[:5, :8])

# for data in englandData:
#    print(data.get('awardedRating').get('ratingLevel'))
#    break

# print(pd.DataFrame(englandData).describe())

# https://hackersandslackers.com/json-into-pandas-dataframes/
# json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
data_df = pd.json_normalize(englandData, sep="_")
print(data_df.head(4))
print(data_df.awardedRating_ratingLevel.head(4))
print(data_df.columns)
print(data_df.describe().transpose())

# https://datatofish.com/k-means-clustering-python/
slim_data_df = pd.DataFrame(
    data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])


kmeans = KMeans(n_clusters=3, init='k-means++').fit(slim_data_df)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(slim_data_df['ratedDwelling_spatialData_totalFloorArea_value'],
            slim_data_df['ratedDwelling_thermalData_finalEnergyDemand_value'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()
