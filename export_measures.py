# coding=utf-8

SENSORS = {
    'BAT': 1,
    'CO2': 2,
    'HUM': 3,
    'PRES': 4,
    'TC': 5,
    'PVT_AIR_IN_H': 6,
    'PVT_AIR_IN_T': 7,
    'PVT_AIR_OUT_T': 8,
    'PVT_AIR_OUT_H': 9,
    'AIR_IN_SPEED': 10,
    'AIR_OUT_SPEED': 11,
    'AIR_IN_VAL1_SP': 12,
    'AIR_IN_VAL1_PV': 13,
    'AIR_IN_VAL2_SP': 14,
    'AIR_IN_VAL2_PV': 15,
    'AIR_OUT_VAL1_SP': 16,
    'AIR_OUT_VAL1_PV': 17,
    'AIR_OUT_VAL2_SP': 18,
    'AIR_OUT_VAL2_PV': 19,
    'PEOPLE_NUMBER': 20,
    'RADIATOR_VAL1': 21,
    'RADIATOR_VAL2': 22,
    'RADIATOR_VAL3': 23,
    'DOOR_STATE': 24,
    'AIR_COND_STATE': 25,
    'RADIATOR_HC_1': 26,
    'RADIATOR_HC_2': 27,
    'RADIATOR_HC_3': 28,
    'AIR_COND_HC': 29
}

import MySQLdb
import json

if __name__ == '__main__':
    db = MySQLdb.connect(user='smart',passwd="password", db="raw_smart")
    c = db.cursor()

    c.execute("""
                select sensor, value, timestamp from poligonsignals where timestamp >= '2018-03-01' order by timestamp ASC
              """)
    res = []
    i = 1
    for elem in c.fetchall():
        name = elem[0].upper()
        if name in SENSORS:
            try:
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
                res.append({
                    "model": "rest.measure",
                    "pk": i,
                    "fields": {
                        "sensor": SENSORS[name],
                        "value": float(val),
                        "timestamp": str(elem[2]),
                    }
                })
                i += 1
            except Exception:
                pass

    with open('fixtures/measures_tail_summer_spring.json', 'w') as f:
        json.dump(res, f)