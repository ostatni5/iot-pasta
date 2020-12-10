from time import time
import paho.mqtt.client as mqtt
from pygame.version import PygameVersion
from device import Device
import pygame ,os
# some_file.py
from utilities.util import *

SCREEN_X = 20 + 300 * 4
SCREEN_Y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Pipeline(Device):
    def __init__(self, throughput=10):
        super().__init__("pipeline")
        self.throughput = throughput
        self.volume = 0
        self.part = 0

    def add(self, product):
        if self.volume == 0:
            self.volume = product.volume
            self.product = product
            return True
        else:
            return False

    def push(self):
        while self.volume > 0:
            self.forward()
            self.part += 1
            self.progress +=1        
        self.running = False
        self.part = 0
        self.product = None
    
    def forward(self):
        step = self.throughput
        if self.volume < step:
            batch = self.volume
            self.volume = 0
        else:
            self.volume -= step
            batch = step
        
        weight = self.product.weight * batch / self.product.volume
        part = {
            "id": self.product.id,
            "type": self.product.type,
            "weight": weight,
            "volume": batch,
            "part": self.part
        }
        mqttc.publish('pasta/log', f"pip install {self.product.id}", 0, True)

        json_part = dict_to_jsonstr(part)
        mqttc.publish('pasta/data/' + devicesForward[self.name], json_part, 0, False)        



pipeline = Pipeline()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, pipeline.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, pipeline)
    elif topics[1] == "data":
        if pipeline.is_on and not pipeline.running:
            pipeline.add(jsonstr_to_obj(payload))
            pipeline.push()


mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()
device = pipeline
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