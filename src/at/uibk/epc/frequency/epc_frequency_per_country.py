from pymongo import MongoClient
from pprint import pprint  # pretty print
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np
import os

# connect to MongoDB
client = MongoClient(
    'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority')
# database
db = client['EPC']
# collection
collection = db.get_collection('EPC_Scottland')

# preparing figure name
country = 'Scottland'
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, country + '_EPC_Plot.png')

pprint(collection.full_name)
# count documents with no filter
pprint(str(collection.count_documents({})) + ' documents aka buildings')
# one json document
# pprint(col.find_one())

# extract only the needed data
dbData = collection.find({},
                         {'awardedRating.ratingLevel': 1, '_id': 0})

print('Extracting data ...')

# convert it into a list
dataFrameList = list()
for d in dbData:
    dataFrameList.append(d['awardedRating']['ratingLevel'])

# load list into a panda dataframe
index = pd.Index(dataFrameList, name="Ratings")
print(index.value_counts())

# sort by rating levels (label) => sort_index
pd.DataFrame(index.value_counts()).sort_index(axis=0, ascending=True).plot(kind='bar', color='green',
                                                                           alpha=0.75, rot=0, legend=False)
plt.title(country)
plt.xlabel('Energy Performance Ratings')
plt.ylabel('Number of buildings')
plt.ylim((0, 300000))
plt.savefig(filename, bbox_inches="tight")

# sort by number of occurences  => sort_values
# index.value_counts().sort_values(axis=0, ascending=True).plot(kind='bar', color='green',
#                                                       alpha=0.75, rot=0)

#bins = np.unique(np.array(dataFrameList))
#print("number of bins " + str(len(bins)))
