
from pymongo import MongoClient
from frequency import epcFrequencyForCountry


def getRawDataScottland():
    scottlandConnectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'
    clientScottland = MongoClient(scottlandConnectionString)
    db = clientScottland['EPC']
    collectionScottland = db.get_collection('EPC_' + 'Scottland')

    print(collectionScottland.full_name)
    print(str(collectionScottland.count_documents({})) +
          ' documents aka buildings')
    # extract only the rating level
    dbData = collectionScottland.find({},
                                      {'awardedRating.ratingLevel': 1, '_id': 0})
    MongoClient.close
    return dbData


def getRawDataIreland():
    irelandConnectionString = 'mongodb+srv://epcuser2:pw12epc559@epcfull-2jvr7.mongodb.net/test?retryWrites=true&w=majority'
    clientIreland = MongoClient(irelandConnectionString)
    db = clientIreland['EPC_Full']
    collectionIreland = db.get_collection('EPC')

    print(collectionIreland.full_name)
    print(str(collectionIreland.count_documents({})) +
          ' documents aka buildings')
    # extract only the rating level
    dbData = collectionIreland.find({},
                                    {'awardedRating.ratingLevel': 1, '_id': 0})
    MongoClient.close
    return dbData


def getRawDataFrance():
    connectionString = 'mongodb+srv://epcuser5:pw15epc@cluster0-929id.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(connectionString)
    db = client['EPC']
    collection = db.get_collection('EPC_' + 'France')

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings')
    # extract only the rating level
    dbData = collection.find({},
                             {'awardedRating.ratingLevel': 1, '_id': 0})
    MongoClient.close
    return dbData


def getRawDataEngland():
    connectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(connectionString)
    db = client['EPC']
    collection = db.get_collection('EPC_' + 'England')

    print(collection.full_name)
    print(str(collection.count_documents({})) +
          ' documents aka buildings')
    # extract only the rating level
    dbData = collection.find({},
                             {'awardedRating.ratingLevel': 1, '_id': 0})
    MongoClient.close
    return dbData


#scottland = 'Scottland'
#epcFrequencyForCountry(getRawDataScottland(), scottland)

ireland = 'Ireland'
epcFrequencyForCountry(getRawDataIreland(), ireland)

#france = 'France'
#epcFrequencyForCountry(getRawDataFrance(), france)

#england = 'England'
#epcFrequencyForCountry(getRawDataEngland(), england)
