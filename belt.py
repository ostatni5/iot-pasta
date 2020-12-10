import random
import time

import paho.mqtt.client as mqtt

from device import Device
from utilities.util import *


class Belt(Device):
    def __init__(self, maxDuration=8, minDuration=0.2, duration=0.5, size=10, segmentCapacity=100):
        super(Belt, self).__init__("Belt")
        self.maxDuration = maxDuration
        self.minDuration = minDuration
        self.size = size
        self.duration = duration
        self.array = [None for i in range(0, self.size)]
        self.name = "belt"

    def alter_duration(self, newDuration=None):
        if newDuration is None:
            self.duration = self.minDuration + random.random() * self.maxDuration
            return
        self.duration = max(min(newDuration, self.maxDuration), self.minDuration)

    def get_speed(self):
        return 1 / self.duration

    def shift_pasta(self):
        last = self.array[-1]
        self.array.pop()
        self.array.insert(0, None)
        return last

    def add(self, element):
        if self.array[0] is None:
            self.array[0] = element
            return True
        else:
            # TODO
            return False

    def move(self):
        time.sleep(self.duration)
        product = self.shift_pasta()
        # mqttc.publish() # product do nast maszyny
        mqttc.publish('pasta/log', f"belt zbeltowal {product}", 0, True)
        mqttc.publish('pasta/data/' + devicesForward[self.name], "dane wysylamy", 0, False)
        print("przesuniete")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, belt.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, belt.name, belt.is_on)
    elif topics[1] == "data":
        if belt.is_on and not belt.running:
            belt.add(jsonstr_to_obj(payload))


belt = Belt()
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

while True:
    print(belt.array)
    belt.move()
    belt.add(random.randint(0, 33))
    print(belt.duration)
    belt.alter_duration()
