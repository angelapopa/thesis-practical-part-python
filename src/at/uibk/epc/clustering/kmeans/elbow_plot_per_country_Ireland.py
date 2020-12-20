from db_data_per_country import getRawData
from elbow_plot import elbow_plot_fct
from elbow_plot import calculate_metrics
import pandas as pd


def elbow_plot_Ireland():
    country = 'Ireland'

    connectionString = 'mongodb+srv://ire_1:t9YjjOigsWGmPTJJ@cluster0.fxx98.mongodb.net/EPC?retryWrites=true&w=majority'
    queryLimit = 90000
    queryThermalDataFields = 'ratedDwelling.thermalData.finalEnergyDemand.value'

    irelandData = getRawData(
        country, connectionString, queryThermalDataFields, queryLimit)

    # https://hackersandslackers.com/json-into-pandas-dataframes/
    # json_normalize has as default separator '.',
    # since we have float numbers in our data, we set the column separator for the normalization to '_'
    data_df = pd.json_normalize(irelandData, sep="_")
    print(data_df.describe)

    # https://datatofish.com/k-means-clustering-python/
    slim_data_df = pd.DataFrame(
        data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', 'ratedDwelling_thermalData_finalEnergyDemand_value'])
    print(slim_data_df.describe().transpose())

    calculate_metrics(slim_data_df, 3, 'Ireland')
    calculate_metrics(slim_data_df, 4, 'Ireland')
    calculate_metrics(slim_data_df, 5, 'Ireland')
    calculate_metrics(slim_data_df, 6, 'Ireland')
    calculate_metrics(slim_data_df, 7, 'Ireland')
    calculate_metrics(slim_data_df, 8, 'Ireland')
    #elbow_plot_fct(slim_data_df, 'Ireland')


elbow_plot_Ireland()
