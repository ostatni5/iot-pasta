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
        "dtime": 15,
        "ctime": 15
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
        "dtime": 15,
        "ctime": 15
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
        "dtime": 15,
        "ctime": 15
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
        "dtime": 15,
        "ctime": 15
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
        "dtime": 15,
        "ctime": 15
    }
}


devicesForward = {
    "fmixer": "steamer",
    "steamer": "mixer",
    "mixer": "pipeline",
    "pipeline": "dryer",
    "dryer": "belt",
    "belt": "lift",
    "lift": "scale",
    "scale": "cooler",
    "cooler": "silos"
}



def parse_control(payload, mqttc, device):
    if payload == "on" and not device.is_on:
        device.is_on = True
    elif payload == "off" and device.is_on:
        device.is_on = False
    mqttc.publish("pasta/log", f'{device.name} is {payload}', 0, True)

def subscribe_setup(mqttc, device):
    mqttc.publish("pasta/log", f'kontroler {device} ozyl', 0, True)
    mqttc.subscribe(f'pasta/{device}e/control')
    mqttc.subscribe(f'pasta/data/{device}')



def jsonstr_to_obj(data):
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

def obj_to_jsonstr(obj):
    return json.dumps(obj.__dict__)

def dict_to_jsonstr(dictionary):
    return json.dumps(dictionary)