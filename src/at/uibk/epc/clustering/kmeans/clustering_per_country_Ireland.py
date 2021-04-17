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

country = 'Ireland'
connectionString = 'mongodb+srv://ire_1:t9YjjOigsWGmPTJJ@cluster0.fxx98.mongodb.net/EPC?retryWrites=true&w=majority'
queryLimit = 90000
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'

dbData = getRawData(
    country, connectionString, queryThermalDataFields, queryLimit)

#k = 7
k = 4
thermalFields = 'ratedDwelling_thermalData_finalEnergyDemand_value'

# Defining border for outlier elimination
floor_area_outlier_upper_border = 15

energy_consumption_upper_border = 25
energy_consumption_lower_border = -5

floor_area_outlier_borders = [
    floor_area_outlier_upper_border]
energy_consumption_outlier_borders = [
    energy_consumption_upper_border, energy_consumption_lower_border]

clustering_kmeans(k, country, dbData, thermalFields, floor_area_outlier_borders,
                  energy_consumption_outlier_borders)
