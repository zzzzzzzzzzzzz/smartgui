# coding=utf-8
import os

HOST = 'http://89.223.95.235/'
API_ROOT = os.path.join(HOST, 'api/')
API_MEASURES = os.path.join(API_ROOT, 'measures/insert_by_sensor_name/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# MYSQL_HOST = ''
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'db'

NEW_DATA_CHECK_TIMEDELTA = 30

SENSORS = [
    'BAT',
    'CO2',
    'HUM',
    'PRES',
    'TC',
    'PVT_AIR_IN_H',
    'PVT_AIR_IN_T',
    'PVT_AIR_OUT_T',
    'PVT_AIR_OUT_H',
    'AIR_IN_SPEED',
    'AIR_OUT_SPEED',
    'AIR_IN_VAL1_SP',
    'AIR_IN_VAL1_PV',
    'AIR_IN_VAL2_SP',
    'AIR_IN_VAL2_PV',
    'AIR_OUT_VAL1_SP',
    'AIR_OUT_VAL1_PV',
    'AIR_OUT_VAL2_SP',
    'AIR_OUT_VAL2_PV',
    'PEOPLE_NUMBER',
    'RADIATOR_VAL1',
    'RADIATOR_VAL2',
    'RADIATOR_VAL3',
    'DOOR_STATE',
    'AIR_COND_STATE',
    'RADIATOR_HC_1',
    'RADIATOR_HC_2',
    'RADIATOR_HC_3',
    'AIR_COND_HC'
]

# You can create and use local_settings file to override global settings
try:
    from local_settings import *
except ImportError as e:
    print("Can't find local_settings.py file for config: {}", e)
    pass
