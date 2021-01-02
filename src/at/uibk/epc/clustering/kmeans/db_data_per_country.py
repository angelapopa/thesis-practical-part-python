from pymongo import MongoClient

# limit is given with limit(x)


def getRawData(country, connectionString, queryThermalDataFields, queryLimit):

    client = MongoClient(connectionString)
    db = client['EPC']

    # workaround for typo in db name
    if (country == 'Scotland'):
        country = 'Scottland'

    collection = db.get_collection('EPC_' + country.capitalize())

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' total documents aka buildings')
    print(str(queryLimit) +
          ' actual documents aka buildings')

    # extract the floorArea, the finalEnergyDemand and the rating level
    dbData = collection.find({},
                             {'ratedDwelling.spatialData.totalFloorArea.value': 1, queryThermalDataFields: 1, 'awardedRating.ratingLevel': 1}) .limit(queryLimit)
    MongoClient.close
    return dbData
