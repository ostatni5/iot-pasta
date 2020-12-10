import paho.mqtt.client as mqtt
import time, random
from device import Device
# some_file.py
from utilities.util import *



class Dryer(Device):
    def __init__(self, floors=3):
        super().__init__("dryer")
        self.products = [[] for i in range(0,floors)]
        self.time = None

    def add(self, product):
        if len(self.products) > 0:
            self.products[0].append(product)
            self.time = pastaData[product.type]["dtime"]
            return True
        else:
            return False

    def shift():
        last = self.products[-1]
        self.products.pop()
        self.products.insert(0, None)
        return last

    def move(self):
        self.running = True
        self.forward()
        self.running = False
    
    def forward(self):
        products = shift()
        for p in products:
            json_part = obj_to_jsonstr(p)
            mqttc.publish('pasta/data/' + devicesForward[self.name], json_part, 0, False)



dryer = Dryer()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, dryer.name)



def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, dryer.name)
    elif topics[1] == "data":
        if dryer.is_on and not dryer.running:
            dryer.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()


start_time = time.time()
while True:
    if dryer.time is not None and time.time() - start_time >= dryer.time:
        start_time = time.time()
        dryer.dry()
    
    time.sleep(1)