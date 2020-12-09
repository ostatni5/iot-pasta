import threading,os
from ui.view import View
import pygame
from time import sleep
from utilities.util import *

import paho.mqtt.client as mqtt

SCREEN_X = 20+ 300*2
SCREEN_Y = 30
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
NAME = "wyparzacz"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)

pygame.init()

ui = View(NAME, SCREEN_WIDTH, SCREEN_HEIGHT)

is_on = False
running = False
job = None
temperature = 20


def make_pasta(mqttc, payload):
    global running
    stopped = False
    i = 100
    running = True
    while i > 0 and not stopped:
        sleep(0.02)
        stopped = check_temp(mqttc)
        i -= 1
    if stopped:
        mqttc.publish('pasta/log', "produkcja zatrzymana na wyparzaczu", 0, False)
        print("piec wylaczony")
    else:
        mqttc.publish('pasta/log', "wyparzacz wyparzył", 0, True)
        mqttc.publish('pasta/product/mieszacz', "dane wysylamy", 0, False)
        print("wygrzane")
    running = False


def check_temp(mqttc):
    global temperature
    if temperature > 30:
        print("proba wylaczenia pieca")
        mqttc.publish('pasta/log', "temperatura na wyparzaczu za wysoka", 0, False)
        return True
    return False


def make_order(payload, mqttc):
    # we o poiwedz jaki to makaron
    print("proba wyparzenia")
    global job
    job = threading.Thread(target=make_pasta, args=(mqttc, payload, ))
    job.start()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    subscribe_setup(mqttc, NAME)

def on_message(client, userdata, msg):
    global running, is_on
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something
    if topics[-1] == "control":
        parse_control(payload, mqttc, NAME, is_on)
    elif topics[1] == "data":
        if is_on and not running:
            make_order(payload, mqttc)

    # end checking topics


mqttc = mqtt.Client()
mqttc.will_set("pasta/log", "kontroler wyparzacza dokonal zywota", 0, True)
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
        "processing": str(job),
        "progres": "0%",
        "status": str(is_on),
        "sensors": [["Temp[C]", str(temperature)]],
    }

    ui.render(state)
    clock.tick(10)


pygame.quit()
