from time import sleep

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # start subscribing to topics
    # example mqttc.subscribe("topic/topic/topic")
    mqttc.publish("pasta/log", "t-sensor-wyparzacz ozyl", 0, True)
    # mqttc.subscribe("pasta/data/wyparzacz/temp")
    # end subscribing to topics


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something

    # end checking topics


mqttc = mqtt.Client("projekt_AC_t-sensor_wyparzacz")
mqttc.will_set("pasta/log", "t-sensor_wyparzacz dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

while True:
    sleep(1)
    mqttc.publish("pasta/data/wyparzacz/temp", "high", 0, False)
