from pymongo import MongoClient
from frequency import getRawData
from frequency import epcFrequencyForCountry

connectionString = 'mongodb+srv://epcuser5:pw15epc@cluster0-929id.mongodb.net/test?retryWrites=true&w=majority'

queryLimit = 100000
Xlimit = 45000
country = 'France'

epcFrequencyForCountry(getRawData(
    country, connectionString, queryLimit), country, queryLimit, Xlimit)
