from pymongo import MongoClient

# limit is given with limit(x)


def getRawDataIreland():
    #connectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
    connectionString = 'mongodb+srv://ire_1:t9YjjOigsWGmPTJJ@cluster0.fxx98.mongodb.net/EPC?retryWrites=true&w=majority'
    client = MongoClient(connectionString)
    db = client['EPC']
    collection = db.get_collection('EPC_' + 'Ireland')

    irelandQueryLimit = 90000

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings available in the database')
    # extract the floorArea, the finalEnergyDemand and the rating level
    dbData = collection.find({},
                             {'ratedDwelling.spatialData.totalFloorArea.value': 1, 'ratedDwelling.thermalData.finalEnergyDemand.value': 1, 'awardedRating.ratingLevel': 1}) .limit(irelandQueryLimit)

    print(str(irelandQueryLimit) +
          ' documents aka buildings taken for analysis')
    MongoClient.close
    return dbData
