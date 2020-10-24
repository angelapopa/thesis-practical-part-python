from pymongo import MongoClient

# limit is given with limit(x)


def getRawDataEngland():
    connectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(connectionString)
    db = client['EPC']
    collection = db.get_collection('EPC_' + 'England')

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings')
    # extract the floorArea, the finalEnergyDemand and the rating level
    dbData = collection.find({},
                             {'ratedDwelling.spatialData.totalFloorArea.value': 1, 'ratedDwelling.thermalData.finalEnergyDemand.value': 1, 'awardedRating.ratingLevel': 1}) .limit(70000)

    MongoClient.close
    return dbData
