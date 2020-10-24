from clustering_models.db_data_per_country import getRawDataFromDB
from clustering_models.clustering_and_saving_radius_models import clusteringAndSavingRadiusModels

scottlandConnectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.primaryEnergyDemand.value'
scottlandCountryString = "Scottland"
scottlandQueryLimit = 70000

dbData = getRawDataFromDB(
    scottlandCountryString, scottlandConnectionString, queryThermalDataFields, scottlandQueryLimit)

clusteringAndSavingRadiusModels(
    scottlandCountryString.lower(), queryThermalDataFields, dbData)
