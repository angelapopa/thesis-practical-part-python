from pathlib import Path
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawDataEngland
import os

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

# https://datatofish.com/k-means-clustering-python/
slim_data_df = pd.DataFrame(
    data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])

# fitting the data is quite important, the clusters are now more like circles; the non-fitted data was more like strapes.
slim_fitted_df = StandardScaler().fit_transform(slim_data_df)
