from threading import Thread
from time import sleep

import paho.mqtt.client as mqtt

running = False
stopped = False
job = None


def check_temp(payload, mqttc):
    global stopped, job
    if payload == "high" and running:
        print("proba wylaczenia pieca")
        mqttc.publish('pasta/log', "temperatura na wyparzaczu za wysoka", 0, False)
        stopped = True


def make_order(payload, mqttc):
    # we o poiwedz jaki to makaron
    global running, stopped
    running = True
    sleep(3)
    running = False
    if stopped:
        mqttc.publish('pasta/log', "produkcja zatrzymana na wyparzaczu", 0, False)
    else:
        mqttc.publish('pasta/log', "wyparzacz wyparzył", 0, True)
        mqttc.publish('pasta/product/mieszacz', "dane wysylamy", 0, False)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # start subscribing to topics
    # example mqttc.subscribe("topic/topic/topic")
    mqttc.publish("pasta/log", "wyparzacz ozyl", 0, True)
    mqttc.subscribe("pasta/product/wyparzacz/order")
    mqttc.subscribe("pasta/data/wyparzacz/temp")
    # end subscribing to topics


def on_message(client, userdata, msg):
    global running, job
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something
    if topics[-1] == "order":
        if not running:
            running = True
            job = Thread(target=make_order, args=(payload, mqttc))
            job.start()
    elif topics[-1] == "temp":
        check_temp(payload, mqttc)

    # end checking topics


mqttc = mqtt.Client("projekt_AC_wyparzacz")
mqttc.will_set("pasta/log", "wyparzacz dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_forever()
