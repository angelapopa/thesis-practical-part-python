from classifying_models.db_data_per_country import getRawDataFromDB
from classifying_models.classifying_and_saving_radius_models import classifyingAndSavingRadiusModels

#franceConnectionString = 'mongodb+srv://epcuser5:pw15epc@cluster0-929id.mongodb.net/test?retryWrites=true&w=majority'
franceConnectionString = 'mongodb+srv://fra_1:Zg8RMRof0PiGOILE@cluster0.o03xt.mongodb.net/EPC?retryWrites=true&w=majority'

queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyConsumption.value'
franceCountryString = "France"

#franceQueryLimit = 80000
franceQueryLimit = 100000

dbData = getRawDataFromDB(
    franceCountryString, franceConnectionString, queryThermalDataFields, franceQueryLimit)

classifyingAndSavingRadiusModels(
    franceCountryString.lower(), queryThermalDataFields, dbData)
