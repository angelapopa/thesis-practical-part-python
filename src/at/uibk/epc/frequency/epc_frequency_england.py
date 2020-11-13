
from pymongo import MongoClient
from frequency import getRawData
from frequency import epcFrequencyForCountry

#connectionString = 'mongodb+srv://epcuser4:pw14epc@cluster0-1w0r9.mongodb.net/test?retryWrites=true&w=majority'
connectionString = 'mongodb+srv://admin:admin@cluster0.ojmf2.mongodb.net/EPC?retryWrites=true&w=majority'

queryLimit = 100000
Xlimit = 45000
country = 'England'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
