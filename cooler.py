import paho.mqtt.client as mqtt
import time, random
from device import Device
import os
import pygame
# some_file.py
from utilities.util import *

SCREEN_X = 20 + 300 * 3
SCREEN_Y = 30 + 330 * 1
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Cooler(Device):
    def __init__(self, floors=4):
        super().__init__("cooler")
        self.products = [[] for i in range(0,floors)]
        self.time = None

    def add(self, product):
        if len(self.products) > 0:
            self.products[0].append(product)
            self.time = pastaData[product.type]["ctime"]
            self.product = product
            return True
        else:
            return False

    def shift(self):
        last = self.products[-1]
        self.products.pop()
        self.products.insert(0, [])
        return last

    def cool(self):
        self.running = True
        self.forward()
        self.running = False
    
    def forward(self):
        products = self.shift()
        for p in products:
            time.sleep(0.5)
            self.product = p
            json_part = obj_to_jsonstr(p)
            mqttc.publish('pasta/data/' + devicesForward[self.name], json_part, 0, False)
        self.progress+=1



cooler = Cooler()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, cooler.name)



def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, cooler)
    elif topics[1] == "data":
        if cooler.is_on and not cooler.running:
            cooler.add(jsonstr_to_obj(payload))


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = cooler
ui = device.ui


start_time = time.time()
while running_ui:
    if len(self.products[0]) + len(self.products[1]) + len(self.products[2]) != 0:
        if cooler.time is not None and time.time() - start_time >= cooler.time:
            cooler.cool()        
            start_time = time.time()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False
    
    if cooler.time is not None:
        time.sleep(cooler.time)
        cooler.cool()

    state = {
        "processing": str(device.product),
        "progres": str(device.progress),
        "status": device.get_status(),
        "sensors": [],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()

