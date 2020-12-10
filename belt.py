from device import Device
import random
import time

from device import Device
import paho.mqtt.client as mqtt
import time, random,os,pygame
from utilities.util import *

SCREEN_X = 20 + 300 * 0
SCREEN_Y = 30 + 330 * 1
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)
pygame.init()


class Belt(Device):
    def __init__(self, maxDuration=8, minDuration=0.2, duration=0.1, size=50, segmentCapacity=100):
        super(Belt, self).__init__("belt")
        self.maxDuration = maxDuration
        self.minDuration = minDuration
        self.size = size
        self.duration = duration
        self.array = [None for i in range(0,self.size)]

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
        if last is not None:
            self.progress+=1
        return last

    def add(self, element):
        if self.array[0] is None:
            self.array[0] = element
            return True
        else:
            return False

    def move(self):
        time.sleep(self.duration)
        self.product = self.shift_pasta()
        # mqttc.publish() # product do nast maszyny
        if self.product is not None:
            mqttc.publish('pasta/log', f"belt zbeltowal {self.product}", 0, True)
            mqttc.publish('pasta/data/' + devicesForward[self.name], obj_to_jsonstr(self.product), 0, False)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, belt.name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    if topics[-1] == "control" or topics[1] == "control":
        parse_control(payload, mqttc, belt)
    elif topics[1] == "data":
        if belt.is_on and not belt.running:
            belt.add(jsonstr_to_obj(payload))


belt = Belt()
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org") 
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

device = belt
ui = device.ui

while running_ui:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

    belt.move()

    state = {
        "processing": str(device.product.id if hasattr(device.product,"id") else None ),
        "progres": str(device.progress),
        "status": device.get_status(),
        "sensors": [],
    }

    ui.render(state)
    clock.tick(10)

pygame.quit()

