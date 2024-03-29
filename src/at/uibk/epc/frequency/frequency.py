from pymongo import MongoClient
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os


def getRawData(country, connectionString, queryLimit):

    client = MongoClient(connectionString)
    db = client['EPC']
    collection = db.get_collection('EPC_' + country)

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings')
    # extract only the rating level
    dbData = collection.find({},
                             {'awardedRating.ratingLevel': 1, '_id': 0}).limit(queryLimit)
    MongoClient.close
    return dbData


def epcFrequencyForCountry(dbData, country, queryLimit, Xlimit):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here + '/plots/', country + '_EPC_Plot.png')
    print('Extracting data ...')

    # convert it into a list
    dataFrameList = list()
    for d in dbData:
        dataFrameList.append(d['awardedRating']['ratingLevel'])

    # load list into a panda dataframe
    index = pd.Index(dataFrameList, name="Ratings")
    print(index.value_counts())
    print("buildings total: " + str(len(dataFrameList)))

    # sort by rating levels (label) => sort_index
    pd.DataFrame(index.value_counts()).sort_index(axis=0, ascending=True).plot(kind='bar', color='green',
                                                                               alpha=0.75, rot=0, legend=False)
    plt.title(country + ": a total of " +
              str(len(dataFrameList)) + " buildings")
    plt.xlabel('Energy Performance Ratings')
    plt.ylabel('Number of buildings')
    plt.ylim((0, Xlimit))
    plt.savefig(filename, bbox_inches="tight")


# sort by number of occurences  => sort_values
# index.value_counts().sort_values(axis=0, ascending=True).plot(kind='bar', color='green',
#                                                       alpha=0.75, rot=0)

#bins = np.unique(np.array(dataFrameList))
#print("number of bins " + str(len(bins)))
