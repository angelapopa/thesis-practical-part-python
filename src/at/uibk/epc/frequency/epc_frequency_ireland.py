from frequency import getRawData
from pymongo import MongoClient
from frequency import epcFrequencyForCountry

#connectionString_not_working = 'mongodb+srv://epcuser2:pw12epc559@epcfull-2jvr7.mongodb.net/test?retryWrites=true&w=majority'
connectionString = 'mongodb+srv://epcuser2:pw12epc559@epcfull.2jvr7.mongodb.net/test?authSource=admin&replicaSet=EpcFull-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'

queryLimit = 565587
Xlimit = 320000
country = 'Ireland'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
