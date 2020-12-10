import os
import pygame
import random
import time

import paho.mqtt.client as mqtt

from device import Device
from utilities.util import *

SCREEN_X = 20 + 300 * 1
SCREEN_Y = 30 + 330 * 1
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Lift(Device):
    def __init__(self, maxDuration=8, minDuration=0.2, duration=0.5, numberOfCarts=10, cartLoad=100):
        super(Lift, self).__init__("lift")
        self.maxDuration = maxDuration
        self.minDuration = minDuration
        self.numberOfCarts = numberOfCarts
        self.duration = duration
        self.array = [None for i in range(0, self.numberOfCarts)]

    def alterDuration(self, newDuration=None):
        if (newDuration == None):
            self.duration = self.minDuration + random.random() * self.maxDuration
            return
        self.duration = max(min(newDuration, self.maxDuration), self.minDuration)

    def getSpeed(self):
        return 1 / self.duration

    def shift(self):
        last = self.array[-1]
        self.array.pop()
        self.array.insert(0, None)
        return last

    def send(self):
        el = self.shift()
        mqttc.publish()

    def add(self, element):
        if (self.array[0] == None):
            self.array[0] = element
            return True
        else:
            # TODO
            return False

    def move(self):

        time.sleep(self.duration)
        self.shift()
        
        
lift = Lift()
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, lift.name)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, lift)
    elif topics[1] == "data":
        if lift.is_on and not lift.running:
            lift.add(jsonstr_to_obj(payload))



mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = lift
ui = device.ui

while running_ui:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    lift.move()
    lift.add(random.randint(0, 33))
    lift.alterDuration()

    state = {
        "processing": str(device.product),
        "progres": str(device.progress),
        "status": device.get_status(),
        "sensors": [],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
