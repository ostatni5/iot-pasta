import paho.mqtt.client as mqtt
from device import Device
import time, random
# some_file.py
from utilities.util import *



class Silos(Device):
    def __init__(self, weight=100):
        super().__init__("silos")
        self.products = []

    def add(self, product):
        self.products.append(product)




silos = Silos()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, silos.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, silos)
    elif topics[1] == "data":
        if silos.is_on:
            silos.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_forever()