from pathlib import Path
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from db_data_per_country import getRawData
from clustering_per_country import clusering_kmeans
import os

country = 'Scotland'
connectionString = 'mongodb+srv://scott_1:JP3JXGuQQC9fkPiZ@cluster0.licv8.mongodb.net/EPC?retryWrites=true&w=majority'
queryLimit = 100000
queryThermalDataFields = 'ratedDwelling.thermalData.primaryEnergyDemand.value'

dbData = getRawData(
    country, connectionString, queryThermalDataFields, queryLimit)

k = 3
thermalFields = 'ratedDwelling_thermalData_primaryEnergyDemand_value'
clusering_kmeans(k, country, dbData, thermalFields)
