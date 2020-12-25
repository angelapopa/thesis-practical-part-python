from classifying_models.db_data_per_country import getRawDataFromDB
from classifying_models.classifying_and_saving_knn_models import classifyingAndSavingKnnModels

#englandConnectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
englandConnectionString = 'mongodb+srv://engl_1:GY9s0BNDrTNjvLFK@cluster0.ojmf2.mongodb.net/EPC?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'
englandCountryString = "England"
# 759464
#englandQueryLimit = 105000
englandQueryLimit = 100000

dbData = getRawDataFromDB(
    englandCountryString, englandConnectionString, queryThermalDataFields, englandQueryLimit)

classifyingAndSavingKnnModels(
    englandCountryString.lower(), queryThermalDataFields, dbData)
