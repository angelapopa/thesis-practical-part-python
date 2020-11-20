from frequency import getRawData
from pymongo import MongoClient
from frequency import epcFrequencyForCountry

#connectionString_not_working = 'mongodb+srv://epcuser2:pw12epc559@epcfull-2jvr7.mongodb.net/test?retryWrites=true&w=majority'
connectionString = 'mongodb+srv://ire_1:t9YjjOigsWGmPTJJ@cluster0.fxx98.mongodb.net/EPC?retryWrites=true&w=majority'

queryLimit = 90000
Xlimit = 35000
country = 'Ireland'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
