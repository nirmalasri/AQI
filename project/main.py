import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time


from projectlib.alldata import CollectData
from projectlib.alldata import PrintData


cities = ["Amarillo", "Lubbock", "Dallas", "Houston", "Austin", "El Paso", "San Antonio", "Corpus Christi", "Abilene", "Fort Worth", "Waco", "McAllen", "Brownsville" ]


# print eighty lines of whatever character is passed
def printeighty(what):
    for i in range(80):
        if i < 79:
            print(what, end='')
        else:
            print(what, end='\n', flush=True)


# MAIN PROGRAM

for city in cities:
    
    collectdata = CollectData()
    result = collectdata.get_datum(city)
    printeighty("*")


    if result["status"] in ["ok", "OK"]:
        printdata = PrintData()    
        printdata.print_attributes_from_data(result)    
    else:
        print("No report")
