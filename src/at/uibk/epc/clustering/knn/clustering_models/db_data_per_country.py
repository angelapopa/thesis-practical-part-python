from pymongo import MongoClient

# limit is given with limit(x)


def getRawDataFromDB(country, connectionString, thermalDataQueryFields, query_limit):
    client = MongoClient(connectionString)
    if country == 'Ireland':
        dbName = 'EPC_Full'
        collectionName = 'EPC'
    else:
        dbName = 'EPC'
        collectionName = 'EPC_' + country.capitalize()

    db = client[dbName]
    collection = db.get_collection(collectionName)

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings')
    # extract the floorArea, the finalEnergyDemand/finaleEnergyConsumption and the rating level
    if (query_limit == 0):
        dbData = collection.find({},
                                 {'ratedDwelling.spatialData.totalFloorArea.value': 1, thermalDataQueryFields: 1, 'awardedRating.ratingLevel': 1})
    else:
        dbData = collection.find({},
                                 {'ratedDwelling.spatialData.totalFloorArea.value': 1, thermalDataQueryFields: 1, 'awardedRating.ratingLevel': 1}) .limit(query_limit)

    MongoClient.close
    return dbData
