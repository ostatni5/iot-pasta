import paho.mqtt.client as mqtt
import time, random
# some_file.py
from utilities.util import *



class Pipeline:
    def __init__(self, throughput=10):
        self.throughput = throughput
        self.volume == 0
        self.is_on = False
        self.running = False
        self.name = "pipeline"

    def add(self, product):
        if self.volume == 0:
            self.volume = product.volume
            self.product = product
            return True
        else:
            return False

    def push(self):
        stopped = False
        
        while self.volume > 0 and not stopped:
            self.forward()
            
            if stopped:
                mqttc.publish('pasta/log', "produkcja zatrzymana na rurze", 0, False)
                print("wyciąg rurowy wylaczony")
        self.running = False
    
    def forward(self):
        step = self.throughput
        if self.volume < step:
            batch = self.volume
            self.volume = 0
        else:
            self.volume -= step
            batch = step
        
        weight = self.product["weight"] * batch / self.product["volume"]
        part = {
            "type": self.product["type"],
            "weight": weight,
            "volume:": batch
        }

        json_part = dict_to_jsonstr(part)
        mqttc.publish('pasta/data/' + devicesForward[self.name], json_part, 0, False)



pipeline = Pipeline()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, pipeline.device)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, pipeline.device, pipeline.is_on)
    elif topics[1] == "data":
        if pipeline.is_on and not pipeline.running:
            pipeline.add(jsonstr_to_obj(payload))
            pipeline.push()


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

while True:
    time.sleep(1)
