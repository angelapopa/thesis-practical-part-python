from clustering_models.db_data_per_country import getRawDataFromDB
from clustering_models.clustering_and_saving_radius_models import clusteringAndSavingRadiusModels

#irelandConnectionString = 'mongodb+srv://epcuser2:pw12epc559@epcfull-2jvr7.mongodb.net/test?retryWrites=true&w=majority'
irelandConnectionString = 'mongodb+srv://ire_1:t9YjjOigsWGmPTJJ@cluster0.fxx98.mongodb.net/EPC?retryWrites=true&w=majority'

queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'
irelandCountryString = "Ireland"

#irelandQueryLimit = 80000
irelandQueryLimit = 90000

dbData = getRawDataFromDB(
    irelandCountryString, irelandConnectionString, queryThermalDataFields, irelandQueryLimit)

clusteringAndSavingRadiusModels(
    irelandCountryString.lower(), queryThermalDataFields, dbData)
