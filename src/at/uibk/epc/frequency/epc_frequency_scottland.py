from frequency import getRawData
from pymongo import MongoClient
from frequency import epcFrequencyForCountry

connectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'

queryLimit = 701461
Xlimit = 320000
country = 'Scottland'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
