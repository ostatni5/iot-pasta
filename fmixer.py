import time

from device import Device
from ui.view import View
import os
import paho.mqtt.client as mqtt
import pygame
from utilities.util import *

SCREEN_X = 20 + 300 * 1
SCREEN_Y = 30
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
NAME = "Orderer"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)

pygame.init()

ui = View(NAME, SCREEN_WIDTH, SCREEN_HEIGHT)


def getTemperature():
    return 90
    # TODO


class FMixer(Device):
    def __init__(self, mix_time=10, maxTemperature=200):
        super().__init__("fmixer")
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

    def mix(self):
        stopped = False
        self.progress = 0
        while self.progress < 100 and not stopped:
            time.sleep(self.mix_time / 100)
            stopped = self.check_temp()
            self.progress += 1
        if stopped:
            mqttc.publish('pasta/log', "produkcja zatrzymana na mieszaczu wstepnym", 0, False)
            print("mieszacz wstepny wylaczony")
        else:
            self.forward()
        self.running = False

    def forward(self):
        mqttc.publish('pasta/log', "mieszacz wstepny zmieszał", 0, True)
        mqttc.publish('pasta/data/wyparzacz', "dane wysylamy", 0, False)
        print("mieszacz zmieszał")
        self.volume = 0

    def check_temp(self):
        temperature = getTemperature()
        if temperature > pastaData[self.product.type]["temperature"]:
            temperature -= 5
        elif temperature > self.maxTemperature:
            print("proba wylaczenia mieszacza wstepnego")
            mqttc.publish('pasta/log', "temperatura na mieszaczu wstepnym za wysoka", 0, False)
            return True
        return False


fmixer = FMixer()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, fmixer.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control":
        parse_control(payload, mqttc, fmixer.name)
    elif topics[1] == "data":
        if fmixer.is_on and not fmixer.running:
            fmixer.add(jsonstr_to_obj(payload))
            fmixer.mix()

    # end checking topics


mqttc = mqtt.Client()
mqttc.will_set("pasta/log", "mieszacz wstepny dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

while running_ui:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    state = {
        "processing": "AAA",
        "progres": "0%",
        "status": str(is_on),
        "sensors": [["CCC", "DDD"]],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
