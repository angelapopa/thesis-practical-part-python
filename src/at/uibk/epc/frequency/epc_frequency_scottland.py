from frequency import getRawData
from pymongo import MongoClient
from frequency import epcFrequencyForCountry

#connectionString = 'mongodb+srv://epcuser3:pw13epc@cluster0-aivtv.mongodb.net/test?retryWrites=true&w=majority'
connectionString = 'mongodb+srv://scott_1:JP3JXGuQQC9fkPiZ@cluster0.licv8.mongodb.net/EPC?retryWrites=true&w=majority'

queryLimit = 100000
Xlimit = 45000
country = 'Scottland'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
