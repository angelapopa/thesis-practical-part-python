from classifying_models.db_data_per_country import getRawDataFromDB
from classifying_models.classifying_and_saving_radius_models import classifyingAndSavingRadiusModels

#scotlandConnectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'
scotlandConnectionString = 'mongodb+srv://scott_1:JP3JXGuQQC9fkPiZ@cluster0.licv8.mongodb.net/EPC?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.primaryEnergyDemand.value'
scotlandCountryString = "Scotland"
scotlandQueryLimit = 100000

dbData = getRawDataFromDB(
    scotlandCountryString, scotlandConnectionString, queryThermalDataFields, scotlandQueryLimit)

classifyingAndSavingRadiusModels(
    scotlandCountryString.lower(), queryThermalDataFields, dbData)
