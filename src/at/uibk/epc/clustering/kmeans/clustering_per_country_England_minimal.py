from pathlib import Path
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawData
from clustering_per_country import clustering_kmeans
import os

# here we use the same amount of input data as for the k-medoids example
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

clustering_kmeans(k, country, dbData, thermalFields,
                  floor_area_outlier_borders, energy_consumption_outlier_borders)
