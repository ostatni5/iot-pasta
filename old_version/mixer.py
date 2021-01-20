import pygame
from old_version.device import Device
import paho.mqtt.client as mqtt
import time
import os
# some_file.py
from old_version.utilities.util import *

SCREEN_X = 20 + 300 * 3
SCREEN_Y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()

def getPressure():
    return 2



def getTemperature():
    return 90



class Mixer(Device):
    def __init__(self, mix_time=2, maxTemperature=200, maxPressure=3):
        super(Mixer, self).__init__("mixer")
        self.volume = 0
        self.mix_time = mix_time
        self.maxPressure = maxPressure
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
            stopped = self.check_temp() or self.check_pressure()
            self.progress += 1
        if stopped:
            mqttc.publish(
                'pasta/log', "produkcja zatrzymana na mieszaczu", 0, False)
            print("mieszacz wylaczony")
        else:
            self.forward()
        self.running = False

    def forward(self):
        mqttc.publish('pasta/log', "mieszacz zmieszal", 0, True)
        mqttc.publish('pasta/data/' +
                      devicesForward[self.name], obj_to_jsonstr(self.product), 0, False)
        self.volume = 0
        self.clear()

    def check_temp(self):
        temperature = getTemperature()
        if temperature > pastaData[self.product.type]["temperature"]:
            temperature -= 5
        elif temperature > self.maxTemperature:
            print("proba wylaczenia mieszacza")
            mqttc.publish(
                'pasta/log', "temperatura na mieszaczu za wysoka", 0, False)
            return True
        return False

    def check_pressure(self):
        pressure = getPressure()
        if pressure > pastaData[self.product.type]["pressure"]:
            pressure -= .10
        elif pressure > self.maxPressure:
            print("proba wylaczenia mieszacza")
            mqttc.publish(
                'pasta/log', "ciśnienie na mieszaczu za wysokie", 0, False)
            return True
        return False


mixer = Mixer()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, mixer.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, mixer)
    elif topics[1] == "data":
        if mixer.is_on and not mixer.running:
            mixer.add(jsonstr_to_obj(payload))
            mixer.mix()


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = mixer
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
        "sensors": [["Temp", str(getTemperature())],
                    ["Press", str(getPressure())]],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()
