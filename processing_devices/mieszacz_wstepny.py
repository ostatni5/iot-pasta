from ui.view import View
import os
import paho.mqtt.client as mqtt
import pygame

SCREEN_X = 20+ 300*1
SCREEN_Y = 30
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
NAME = "Orderer"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_X, SCREEN_Y)

pygame.init()

ui = View(NAME, SCREEN_WIDTH, SCREEN_HEIGHT)

is_on = False


def make_order(payload, mqttc):
    # we o poiwedz jaki to makaron
    mqttc.publish('pasta/log', "mieszacz wstepny zrobil makaron", 0, True)
    mqttc.publish('pasta/data/wyparzacz', "makaron z mieszacza wstepnego", 0, False)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # start subscribing to topics
    # example mqttc.subscribe("topic/topic/topic")
    mqttc.publish("pasta/wyparzacz/control", "on", 0, True)
    mqttc.publish("pasta/log", "mieszacz stepny ozyl", 0, True)
    mqttc.subscribe("pasta/mieszacz_wstepny/control")
    mqttc.subscribe("pasta/data/mieszacz_wstepny")
    # end subscribing to topics


def parse_control(payload, mqttc):
    global is_on
    if payload == "on" and not is_on:
        is_on = True
    elif payload == "off" and is_on:
        is_on = False
    mqttc.publish("pasta/log", f'mieszacz_wstepny is {payload}', 0, True)


def on_message(client, userdata, msg):
    global is_on
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something
    if topics[-1] == "control":
        parse_control(payload, mqttc)
    elif topics[1] == "data" and is_on:
        make_order(payload, mqttc)

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