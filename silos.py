import paho.mqtt.client as mqtt
from device import Device
import time, random
import os
import pygame
# some_file.py
from utilities.util import *

SCREEN_X = 20 + 300 * 4
SCREEN_Y = 30 + 330 * 1
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()

class Silos(Device):
    def __init__(self, weight=100):
        super().__init__("silos")
        self.products = []

    def add(self, product):
        self.products.append(product)
        mqttc.publish('pasta/log', f"silos brrr {product}", 0, True)
        self.progress+=1




silos = Silos()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, silos.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, silos)
    elif topics[1] == "data":
        if silos.is_on:
            silos.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = silos
ui = device.ui

while running_ui:

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