import joblib
from sklearn.neighbors import RadiusNeighborsClassifier
from operator import itemgetter
import operator
from sklearn.model_selection import GridSearchCV
from pathlib import Path
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier

# TODO split this in more funtions


def clusteringAndSavingRadiusModels(country, thermalDataQueryFields, dbData):

    # https://hackersandslackers.com/json-into-pandas-dataframes/
    # json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
    data_df = pd.json_normalize(dbData, sep="_")
    print(data_df.describe().transpose())
    print(data_df.head())

    print("nr. of elements considered: ")
    print(len(data_df.index))

    # save dataframe to file for later use, for the api
    filenameRadiusDf = "serialized_radius_dataframe_" + country + ".pck"
    saveFile(country, filenameRadiusDf, data_df)

    # triming down the dataframe
    thermalDataColumn = thermalDataQueryFields.replace('.', '_')
    # forcing datatype due to memory issues
    # TODO: does this work
    slim_data_df = pd.DataFrame(
        data_df, columns=['ratedDwelling_spatialData_totalFloorArea_value', thermalDataColumn]).astype(np.dtype('uint32'))
    print(slim_data_df.head())

    # forcing datatype due to memory issues
    # labels_df = pd.DataFrame(
    # data_df, columns = ['awardedRating_ratingLevel']).astype(np.dtype('U', 1))
    labels_df = pd.DataFrame(
        data_df, columns=['awardedRating_ratingLevel'])  # .astype(np.dtype('U', 1))
    print(labels_df.head())

    X = slim_data_df
    y = labels_df.values.ravel()  # collapse array into one dimension

    # split the data in test and train data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    print("split done")

    # fitting the data is quite important
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # saving scaler for later use
    scalerFilename = "serialized_radius_scaler_" + country + ".pck"
    saveFile(country, scalerFilename, scaler)

    # the radius neighbors
    # https: // scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html

    classifier_radius = RadiusNeighborsClassifier(
        radius=5, metric='euclidean', weights='distance')
    # A classifier cannot classify the samples of a class if some samples of the class aren't present in the training set
    classifier_radius.set_params(outlier_label='Z')
    classifier_radius.fit(X_train, y_train)
    y_pred_radius = classifier_radius.predict(X_test)

    print("radius prediction")
    print(y_pred_radius)

    print("Accuracy radius classifier")
    print(confusion_matrix(y_test, y_pred_radius))
    print(classification_report(y_test, y_pred_radius))

    # joblib - save model to file
    filenameRadiusClassifier = "serialized_radius_classifier_" + country + ".pck"
    saveFile(country, filenameRadiusClassifier, classifier_radius)
    return "finished"


def saveFile(country, fileName, objectToSave):
    here = os.path.dirname(os.path.abspath(__file__))

    filePath = os.path.join(
        Path(here).parent, 'persisted_models', country, fileName)
    joblib.dump(objectToSave, filePath)

    return "file saved"
