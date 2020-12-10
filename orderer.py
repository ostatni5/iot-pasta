import os

import paho.mqtt.client as mqtt
import pygame
from utilities.util import *


from ui.controllView import ControllView

SCREEN_X = 20
SCREEN_Y = 30

NAME = "Orderer"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)

pygame.init()

ui = ControllView(NAME)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # start subscribing to topics
    amount = 200
    part = {
        "id": "pasta po prostu",
        "type": "Fusilli",
        "weight": pastaData["Fusilli"]["density"]*amount,
        "volume:": amount
    }
    json_part = dict_to_jsonstr(part)
    mqttc.publish("pasta/log", "orderera ozyl", 0, True)
    mqttc.publish("pasta/data/"+devicesForward["orderer"], json_part, 0, False)
    # end subscribing to topics
    
                    
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")


mqttc = mqtt.Client()
mqttc.will_set("pasta/log", "orderder dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

running_ui = True
clock = pygame.time.Clock()

while running_ui:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mqttc.loop_stop()
            running_ui = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ui.button_on.inside(mouse[0], mouse[1]):
                mqttc.publish('pasta/control', "on", 2, False)

    state = {
        "processing": "AAAA",
        "progres": "0%",
        "status": "BBB",
        "sensors": [["CCC", "DDD"]],
    }

    ui.render(state, mouse)
    clock.tick(10)

pygame.quit()
