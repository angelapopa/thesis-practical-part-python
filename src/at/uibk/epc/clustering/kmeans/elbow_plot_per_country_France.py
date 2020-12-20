
from elbow_plot import elbow_plot_fct
from elbow_plot import calculate_metrics
import pandas as pd


from db_data_per_country import getRawData


def elbow_plot_France():
    country = 'France'

    connectionString = 'mongodb+srv://fra_1:Zg8RMRof0PiGOILE@cluster0.o03xt.mongodb.net/EPC?retryWrites=true&w=majority'
    queryLimit = 100000
    queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyConsumption.value'

    franceData = getRawData(
        country, connectionString, queryThermalDataFields, queryLimit)

    # https://hackersandslackers.com/json-into-pandas-dataframes/
    # json_normalize has as default separator '.',
    # since we have float numbers in our data, we set the column separator for the normalization to '_'
    data_df = pd.json_normalize(franceData, sep="_")
    print(data_df.describe)

    # https://datatofish.com/k-means-clustering-python/
    slim_data_df = pd.DataFrame(
        data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyConsumption_value'])
    print(slim_data_df.describe().transpose())

    calculate_metrics(slim_data_df, 3, 'France')
    calculate_metrics(slim_data_df, 4, 'France')
    calculate_metrics(slim_data_df, 5, 'France')
    calculate_metrics(slim_data_df, 6, 'France')
    calculate_metrics(slim_data_df, 7, 'France')
    calculate_metrics(slim_data_df, 8, 'France')
    #elbow_plot_fct(slim_data_df, 'France')


elbow_plot_France()
