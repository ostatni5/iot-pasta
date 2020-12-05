def main():
    import paho.mqtt.client as mqtt

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # start subscribing to topics
        # example mqttc.subscribe("topic/topic/topic")

        # end subscribing to topics

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        topics = msg.topic.split('/')
        payload = msg.payload.decode("utf-8")
        # check topics and do something

        # end checking topics

    mqttc = mqtt.Client("projekt_AC_9207780821")
    mqttc.will_set("floor_1/service", "C5 is dead", 0, False)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.connect("test.mosquitto.org")
    mqttc.loop_forever()
