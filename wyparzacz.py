import threading
from time import sleep

import paho.mqtt.client as mqtt

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
    # start subscribing to topics
    # example mqttc.subscribe("topic/topic/topic")
    mqttc.publish("pasta/log", "kontroler wyparzacza ozyl", 0, True)
    mqttc.subscribe("pasta/wyparzacz/control")
    mqttc.subscribe("pasta/data/wyparzacz")
    # end subscribing to topics


def parse_control(payload, mqttc):
    global is_on
    if payload == "on" and not is_on:
        is_on = True
    elif payload == "off" and is_on:
        is_on = False
    mqttc.publish("pasta/log", f'wyparzacz is {payload}', 0, True)


def on_message(client, userdata, msg):
    global running, is_on
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something
    if topics[-1] == "control":
        parse_control(payload, mqttc)
    elif topics[1] == "data":
        if is_on and not running:
            make_order(payload, mqttc)

    # end checking topics


mqttc = mqtt.Client()
mqttc.will_set("pasta/log", "kontroler wyparzacza dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_forever()
