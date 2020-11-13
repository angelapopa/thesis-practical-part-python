from clustering_models.db_data_per_country import getRawDataFromDB
from clustering_models.clustering_and_saving_radius_models import clusteringAndSavingRadiusModels

#englandConnectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
englandConnectionString = 'mongodb+srv://admin:admin@cluster0.ojmf2.mongodb.net/EPC?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'
englandCountryString = "England"
# 759464
englandQueryLimit = 105000

dbData = getRawDataFromDB(
    englandCountryString, englandConnectionString, queryThermalDataFields, englandQueryLimit)

clusteringAndSavingRadiusModels(
    englandCountryString.lower(), queryThermalDataFields, dbData)
