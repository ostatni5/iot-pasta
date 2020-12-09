import json
from types import SimpleNamespace

pastaData = {
    "Fusilli": {
        "temperature": 150,
        "pressure": 1.2,
        "ingredients":{
            "eggs": 5,
            "flour": 2,
            "oil": 2
        },
        "density": 1.2,
        "dtime": 1,
        "ctime": 1
    },
    "Spaghetti":{
        "temperature": 150,
        "pressure": 1.2,
        "ingredients":{
            "eggs": 0,
            "flour": 2,
            "oil": 3
        },
        "density": 1.2,
        "dtime": 1,
        "ctime": 1
    },
    "Bigoli":{
        "temperature": 150,
        "pressure": 1.2,
        "ingredients":{
            "eggs": 1,
            "flour": 2,
            "oil": 1
        },
        "density": 1.2,
        "dtime": 1,
        "ctime": 1
    },
    "Gnocchi":{
        "temperature": 150,
        "pressure": 1.2,
        "ingredients":{
            "eggs": 0,
            "flour": 3,
            "oil": 3
        },
        "density": 1.2,
        "dtime": 1,
        "ctime": 1
    },
    "Riccioli":{
        "temperature": 150,
        "pressure": 1.2,
        "ingredients":{
            "eggs": 2,
            "flour": 2,
            "oil": 3
        },
        "density": 1.2,
        "dtime": 1,
        "ctime": 1
    }
}

def parse_control(payload, mqttc, device, is_on):
    if payload == "on" and not is_on:
        is_on = True
    elif payload == "off" and is_on:
        is_on = False
    mqttc.publish("pasta/log", f'{device} is {payload}', 0, True)

def subscribe_setup(mqttc, device):
    mqttc.publish("pasta/log", f'kontroler {device} ozyl', 0, True)
    mqttc.subscribe(f'pasta/{device}e/control')
    mqttc.subscribe(f'pasta/data/{device}')



def jsonstr_to_obj(json):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

def obj_to_jsonstr(obj):
    return json.dumps(obj.__dict__)

def dict_to_jsonstr(dictionary):
    json.dumps(dictionary)