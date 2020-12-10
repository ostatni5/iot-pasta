import paho.mqtt.client as mqtt
import time, random
from device import Device
# some_file.py
from utilities.util import *



class Cooler(Device):
    def __init__(self, floors=4):
        super().__init__("cooler")
        self.products = [[] for i in range(0,floors)]
        self.time = None

    def add(self, product):
        if len(self.products) > 0:
            self.products[0].append(product)
            self.time = pastaData[product.type]["ctime"]
            return True
        else:
            return False

    def shift(self):
        last = self.products[-1]
        self.products.pop()
        self.products.insert(0, None)
        return last

    def move(self):
        self.running = True
        self.forward()
        self.running = False
    
    def forward(self):
        products = self.shift()
        for p in products:
            json_part = obj_to_jsonstr(p)
            mqttc.publish('pasta/data/' + devicesForward[self.name], json_part, 0, False)



cooler = Cooler()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, cooler.name)



def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, cooler)
    elif topics[1] == "data":
        if cooler.is_on and not cooler.running:
            cooler.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()


while True:
    if cooler.time is not None:
        time.sleep(cooler.time)
        cooler.dry()