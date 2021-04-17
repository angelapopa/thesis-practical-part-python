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
country = 'France'
connectionString = 'mongodb+srv://fra_1:Zg8RMRof0PiGOILE@cluster0.o03xt.mongodb.net/EPC?retryWrites=true&w=majority'
queryLimit = 25000
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyConsumption.value'

dbData = getRawData(
    country, connectionString, queryThermalDataFields, queryLimit)

k = 4
thermalFields = 'ratedDwelling_thermalData_finalEnergyConsumption_value'

# Defining border for outlier elimination
floor_area_outlier_upper_border = 10

energy_consumption_upper_border = 3
energy_consumption_lower_border = -5

floor_area_outlier_borders = [
    floor_area_outlier_upper_border]
energy_consumption_outlier_borders = [
    energy_consumption_upper_border, energy_consumption_lower_border]

kmedoids_clustering(country, dbData, thermalFields,
                    k,  floor_area_outlier_borders, energy_consumption_outlier_borders)
