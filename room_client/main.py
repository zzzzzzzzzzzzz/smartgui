# coding=utf-8
import json
from urllib import request

import MySQLdb
import math

from .settings import *
from time import sleep
from datetime import datetime

if __name__ == '__main__':
    db = MySQLdb.connect(user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE)
    c = db.cursor()
    current_tsp = datetime.now() # initial timestamp
    current_id = math.inf
    while True:
        c.execute("""
                    select sensor, 
                           value, 
                           timestamp,
                           id 
                    from poligonsignals 
                    where timestamp > '{}' 
                    order by timestamp ASC
                  """.format(current_tsp.strftime('%Y-%m-%d %H-%M-%S')))

        for elem in c.fetchall(): # check if there are new records exist
            name = elem[0].upper()
            if name in SENSORS:
                try:
                    if elem[2] > current_tsp or int(elem[4]) > current_id:
                        val = elem[1]
                        if name == 'DOOR_STATE':
                            if elem[1] == 'CLOSE':
                                val = 0.0
                            if elem[1] == 'OPEN':
                                val = 1.0
                        if elem[1] == 'FALSE':
                            val = 0.0
                        if elem[1] == 'TRUE':
                            val = 1.0
                        current_tsp = elem[2]
                        current_id = elem[3]
                        data = {
                            'sensor':name,
                            'value': val,
                            'timestamp': elem[2],
                            'room_name': ROOM_NAME
                        }
                        params = json.dumps(data).encode('utf8')
                        req = request.Request(API_MEASURES, data=params,
                                              headers={'content-type': 'application/json'})
                        response = request.urlopen(req) # send new records via api
                except Exception:
                    pass

        sleep(NEW_DATA_CHECK_TIMEDELTA)  # every n seconds

        # Alternative: check if it's possible to run python scripts via mysql db triggers
        # Not so universal and comprehensive but less hacky and bootledgy
        # https://stackoverflow.com/questions/23382499/run-python-script-on-database-event

