from typing import List
import paho.mqtt.client as mqtt
import time
import random
import os
import pygame
from device import Device
# some_file.py
from utilities.util import *

SCREEN_X = 20 + 300 * 5
SCREEN_Y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Dryer(Device):
    def __init__(self, floors=3):
        super().__init__("dryer")
        self.products = [[],[],[]]
        self.time = None

    def add(self, product):
        if len(self.products) > 0:
            self.products[0].append(product)
            self.time = pastaData[product.type]["dtime"]
            self.product = product
            return True
        else:
            return False

    def shift(self):
        last = self.products[-1]
        self.products.pop()
        self.products.insert(0, [])
        return last

    def dry(self):
        self.running = True
        self.forward()
        self.running = False

    def forward(self):
        products = self.shift()
        if len(products) >0:
            self.progress+=1
            for p in products:
                time.sleep(0.5)
                self.product = p
                mqttc.publish('pasta/log', f"dryyyy zbeltowal {p}", 0, True)
                json_part = obj_to_jsonstr(p)
                mqttc.publish('pasta/data/' +
                              devicesForward[self.name], json_part, 2, False)
            


dryer = Dryer()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, dryer.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, dryer)
    elif topics[1] == "data":
        if dryer.is_on and not dryer.running:
            dryer.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()
device = dryer
ui = device.ui


start_time = time.time()
while running_ui:
    if len(device.products[0]) + len(device.products[1]) + len(device.products[2]) != 0:
        if dryer.time is not None and time.time() - start_time >= dryer.time:
            dryer.dry()        
            start_time = time.time()
    else:
        start_time = time.time()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    state = {
        "processing": str(device.product.id if hasattr(device.product,"id") else None ),
        "progres": str(device.progress),
        "status": device.get_status(),
        "sensors": [],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
