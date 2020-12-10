import threading, os
import time

from device import Device
from ui.view import View
import pygame
from time import sleep
from utilities.util import *

import paho.mqtt.client as mqtt

SCREEN_X = 20 + 300 * 2
SCREEN_Y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)

pygame.init()



def getTemperature():
    return 90
    # TODO


class Steamer(Device):
    def __init__(self, mix_time=2, maxTemperature=200):
        super().__init__("steamer")
        self.volume = 0
        self.mix_time = mix_time
        self.maxTemperature = maxTemperature

    def add(self, product):
        if self.volume == 0:
            self.volume = product.volume
            self.product = product
            return True
        else:
            return False

    def steam(self):
        stopped = False
        self.progress = 0
        while self.progress < 100 and not stopped:
            time.sleep(self.mix_time / 100)
            stopped = self.check_temp()
            self.progress += 1
        if stopped:
            mqttc.publish('pasta/log', "produkcja zatrzymana na wyparzaczu", 0, False)
            print("piec wylaczony")
        else:
            self.forward()
        self.running = False

    def forward(self):
        mqttc.publish('pasta/log', "wyparzacz wyparzyl", 0, True)
        mqttc.publish('pasta/data/'+ devicesForward[self.name], obj_to_jsonstr(self.product), 0, False)
        print("wygrzane")
        self.volume = 0
        self.clear()

    def check_temp(self):
        temperature = getTemperature()
        if temperature > pastaData[self.product.type]["temperature"]:
            temperature -= 5
        elif temperature > self.maxTemperature:
            print("proba wylaczenia pieca")
            mqttc.publish('pasta/log', "temperatura na wyparzaczu za wysoka", 0, False)
            return True
        return False


steamer = Steamer()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, steamer.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, steamer)
    elif topics[1] == "data":
        if steamer.is_on and not steamer.running:
            steamer.add(jsonstr_to_obj(payload))
            steamer.steam()

    # end checking topics


mqttc = mqtt.Client()
mqttc.will_set("pasta/log", "kontroler wyparzacza dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = steamer
ui = device.ui

while running_ui:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    state = {
        "processing": str(device.product.id if hasattr(device.product,"id") else None ),
        "progres": str(device.progress)+"%",
        "status": device.get_status(),
        "sensors": [["Temp", str(getTemperature())]],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
