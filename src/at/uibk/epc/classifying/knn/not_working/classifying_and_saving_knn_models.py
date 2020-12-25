import joblib
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
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsRegressor

# TODO split this in more funtions


def classifyingAndSavingKnnModels(country, thermalDataQueryFields, dbData):

    # https://hackersandslackers.com/json-into-pandas-dataframes/
    # json_normalize has as default separator '.', since we have float numbers in our data, we set the column separator for the normalization to '_'
    data_df = pd.json_normalize(dbData, sep="_")
    print(data_df.describe().transpose())
    print(data_df.head())

    print("nr. of elements considered: ")
    print(len(data_df.index))

    # save dataframe to file for later use, for the api
    filenameKnnDf = "serialized_knn_dataframe_" + country + ".pck"
    saveFile(country, filenameKnnDf, data_df)

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

    # https://stackoverflow.com/questions/43162506/undefinedmetricwarning-f-score-is-ill-defined-and-being-set-to-0-0-in-labels-wi
    #y_test = np.array(y_test)
    #y_train = np.array(y_train)

    # fitting the data is quite important
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # saving scaler for later use
    scalerFilename = "serialized_knn_scaler_" + country + ".pck"
    saveFile(country, scalerFilename, scaler)

    # the nearest neighbors
    # https: // scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html

    classifier_knn = KNeighborsClassifier(n_neighbors=5)
    classifier_knn.fit(X_train, y_train)

    y_pred_knn = classifier_knn.predict(X_test)

    print("knn prediction")
    print(y_pred_knn)
    print("accuracy score")
    print(accuracy_score(y_pred_knn, y_test))

    print("Confusion matrix")
    print(confusion_matrix(y_test, y_pred_knn))
    print("Classification report")
    # y_test ist the ground truth
    print(classification_report(y_test, y_pred_knn))

    # Running KNN for various values of n_neighbors and storing results
    knn_r_acc = []
    for i in range(1, 11, 1):
        knn = KNeighborsRegressor(n_neighbors=i)
        knn.fit(X_train, y_train)
        test_score = knn.score(X_test, y_test)
        train_score = knn.score(X_train, y_train)
        knn_r_acc.append(i, test_score, train_score)

    df = pd.DataFrame(knn_r_acc, columns=['K', 'Test Score', 'Train Score'])
    print(df)

    # joblib - save model to file
    filenameKnnClassifier = "serialized_knn_classifier_" + country + ".pck"
    saveFile(country, filenameKnnClassifier, classifier_knn)
    return "finished"


def saveFile(country, fileName, objectToSave):
    here = os.path.dirname(os.path.abspath(__file__))

    filePath = os.path.join(
        Path(here).parent, 'persisted_models', country, fileName)
    joblib.dump(objectToSave, filePath)

    return "file saved"
