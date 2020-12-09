import paho.mqtt.client as mqtt


def make_order(payload, mqttc):
    # we o poiwedz jaki to makaron
    mqttc.publish('pasta/log', "mieszacz wstepny zrobil makaron", 0, True)
    mqttc.publish('pasta/product/wyparzacz/order', "dane wysylamy", 0, False)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # start subscribing to topics
    # example mqttc.subscribe("topic/topic/topic")
    mqttc.publish("pasta/log", "mieszacz stepny ozyl", 0, True)
    mqttc.subscribe("pasta/product/mieszacz_wstepny/order")
    # end subscribing to topics


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")
    # check topics and do something
    if topics[-1] == "order":
        make_order(payload, mqttc)

    # end checking topics


mqttc = mqtt.Client("projekt_AC_mieszacz wstepny")
mqttc.will_set("pasta/log", "mieszacz wstepny dokonal zywota", 0, True)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_forever()
