from clustering_models.db_data_per_country import getRawDataFromDB
from clustering_models.clustering_and_saving_radius_models import clusteringAndSavingRadiusModels

irelandConnectionString = 'mongodb+srv://epcuser2:pw12epc559@epcfull-2jvr7.mongodb.net/test?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'
irelandCountryString = "Ireland"
irelandQueryLimit = 70000

dbData = getRawDataFromDB(
    irelandCountryString, irelandConnectionString, queryThermalDataFields, irelandQueryLimit)

clusteringAndSavingRadiusModels(
    irelandCountryString.lower(), queryThermalDataFields, dbData)
