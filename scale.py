import paho.mqtt.client as mqtt
from device import Device
import time
import random
import os
import pygame
# some_file.py
from utilities.util import *

SCREEN_X = 20 + 300 * 2
SCREEN_Y = 30 + 330 * 1
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Scale(Device):
    def __init__(self, weight=200):
        super().__init__("scale")
        self.weight = weight

    def add(self, product):
        if(self.product is None):
            self.product = product
        elif product is not None:
            self.product.weight += product.weight
            self.product.volume += product.volume

        return True

    def push(self):
        self.running = True
        if self.product.weight >= pastaData[self.product.type]["density"]*self.weight:
            self.forward()
        else:
            self.progress = self.product.weight / self.weight
        self.running = False

    def forward(self):
        json_part = obj_to_jsonstr(self.product)
        mqttc.publish('pasta/log', f"wagam waguje ", 0, True)
        mqttc.publish('pasta/data/' +
                      devicesForward[self.name], json_part, 2, False)
        self.clear()


scale = Scale()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, scale.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, scale)
    elif topics[1] == "data":
        if scale.is_on and not scale.running:
            scale.add(jsonstr_to_obj(payload))
            scale.push()


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = scale
ui = device.ui

while running_ui:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    state = {
        "processing": str(device.product.id if hasattr(device.product, "id") else None),
        "progres": str(device.progress),
        "status": device.get_status(),
        "sensors": [],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
