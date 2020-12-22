from classifying_models.db_data_per_country import getRawDataFromDB
from classifying_models.classifying_and_saving_radius_models import classifyingAndSavingRadiusModels

#scottlandConnectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'
scottlandConnectionString = 'mongodb+srv://scott_1:JP3JXGuQQC9fkPiZ@cluster0.licv8.mongodb.net/EPC?retryWrites=true&w=majority'
queryThermalDataFields = 'ratedDwelling.thermalData.primaryEnergyDemand.value'
scottlandCountryString = "Scottland"
scottlandQueryLimit = 100000

dbData = getRawDataFromDB(
    scottlandCountryString, scottlandConnectionString, queryThermalDataFields, scottlandQueryLimit)

classifyingAndSavingRadiusModels(
    scottlandCountryString.lower(), queryThermalDataFields, dbData)
