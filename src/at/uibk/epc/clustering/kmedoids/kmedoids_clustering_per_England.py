from db_data_per_country import getRawData
from kmedoids_clustering_per_country import kmedoids_clustering
from sklearn_extra.cluster import KMedoids
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# limit 40.000 is ok but takes a lot of time to process and cluster 3 is empty for k=5.
# limit 10.000, cluster=5, inertia aprox 5300
#limit = 10000
#clusters = 5

# due to memory issues, the same amount of input data as for k-means is not usable for kmedoids
country = 'England'
connectionString = 'mongodb+srv://engl_1:GY9s0BNDrTNjvLFK@cluster0.ojmf2.mongodb.net/EPC?retryWrites=true&w=majority'
queryLimit = 20000
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'

dbData = getRawData(
    country, connectionString, queryThermalDataFields, queryLimit)

k = 5
thermalFields = 'ratedDwelling_thermalData_finalEnergyDemand_value'

# Defining border for outlier elimination
floor_area_outlier_upper_border = 15

energy_consumption_upper_border = 12
energy_consumption_lower_border = -5

floor_area_outlier_borders = [
    floor_area_outlier_upper_border]
energy_consumption_outlier_borders = [
    energy_consumption_upper_border, energy_consumption_lower_border]


kmedoids_clustering(country, dbData, thermalFields, k,
                    floor_area_outlier_borders, energy_consumption_outlier_borders)
