import requests
import json
import pymysql
from requests.auth import HTTPBasicAuth
from datetime import datetime
from projectlib import config

# CollectData class

# https://api.waqi.info/feed/['city']/?token=

# from Air Quality open data platform, collect air quality index for different cities in USA

# aqi is the air quality index


class DataStruct:

    def __init__(self, timeid, status, aqi, idx, cityname, cityurl):
        self.timeid = datetime.fromtimestamp(timeid)
        self.aqi = aqi
        self.idx = idx
        self.cityname = cityname
        self.cityurl = cityurl


class CollectData:

    def __init__(self):

       self.key = config.FA_KEY

    # obtains data - connects to json
    def get_datum(self, city):

        # service URL
        url = "https://api.waqi.info/feed/{0}/?token=" + self.key
        url = url.format(city)
        print(url)

        # make request to flight aware
        req = requests.get(url)

        # translate response to JSON

        jsonresult = req.json()

                     
        return jsonresult

class PrintData:

     def print_attributes_from_data(self, fametarjson):

        # parse elements
        aqi = fametarjson["data"]["aqi"]
        idx = fametarjson["data"]["idx"]
        cityurl = fametarjson["data"]["city"]["url"]
        cityname = fametarjson["data"]["city"]["name"]

        output = "City: {3} at {1}\n" + \
                 "aqi: {0} \n" + \
                 "idx: {1} \n" + \
                 "url: {2}\n" 
                 
        output = output.format(aqi, idx, cityurl, cityname)

        print(output)

        db = pymysql.connect(config.FAL_DBHOST,
                             config.FAL_DBUSER,
                             config.FAL_DBPASS,
                             config.FAL_DBNAME)

        # prepare a cursor object
        cursor = db.cursor()

               
        # prepare SQL statement
        statement = "INSERT INTO aqidata(TIMEID, AQI, IDX, CITYNAME, CITYURL)" + \
                    " VALUES (%s, %s, %s,%s, %s)"

        timeid = datetime.now()

        data = (timeid, aqi, idx, cityname, cityurl)

        # give it a shot
        try:
            # Execute the SQL command
            cursor.execute(statement, data)
            # commit/save changes
            db.commit()
        except Exception as exp:
            # rollback changes in case of error
            print('things went bad: ' + str(exp))
            db.rollback()

        # disconnect from server
        db.close()

        return
