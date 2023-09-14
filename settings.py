import json
import os

def read_settings():
    if not os.path.isfile('settings.json'):
        with open('settings.json', mode='w') as stg: 
            stg.write(r'''
{
    "verbose": 0,
    "reconnect": 10,
    "snapshots per page": 5
}
''')
        return {
    "verbose": 0,
    "reconnect": 10,
    "snapshots per page": 5
}
            
    with open('settings.json', mode='r') as stg:
        sdict = json.load(stg)
        return sdict

def get_setting(key):
    return read_settings()[key]

def set_setting(key, value):
    settings = read_settings()
    settings[key] = value
    with open('settings.json', mode='w') as stg:
        json.dump(settings, stg)
