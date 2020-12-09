import paho.mqtt.client as mqtt
import time, random
from util import pastaData

def getPressure():
    return 2
    # TODO

def getTemperature():
    return 90
    # TODO



class Mixer:
    def __init__(self, mix_time = 10, maxTemperature=200, maxPressure=3):
        self.volume = 0
        self.mix_time = mix_time
        self.maxPressure = maxPressure
        self.maxTemperature = maxTemperature

    def add(self, product):
        if self.volume == 0:
            self.volume = product.volume
            self.product = product
            return True
        else:
            return False

    def mix(self):
        time.sleep(self.mix_time)
        
    def forward(self):
        # mqttc.publish() # do rurururkowca
        self.volume = 0
        pass

    def check_temp(self):
        temperature = getTemperature()
        if temperature > pastaData[self.product.type]["temperature"]:
            temperature -= 5
        elif temperature > self.maxTemperature:
            print("proba wylaczenia mieszacza")
            mqttc.publish('pasta/log', "temperatura na mieszaczu za wysoka", 0, False)
            return True
        return False

    def check_pressure(self):
        pressure = getPressure()
        if pressure > pastaData[self.product.type]["pressure"]:
            pressure -= .10
        elif pressure > self.maxPressure:
            print("proba wylaczenia mieszacza")
            mqttc.publish('pasta/log', "ciśnienie na mieszaczu za wysokie", 0, False)
            return True
        return False
    

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #mqttc.subscribe("pasta/log")
    #mqttc.subscribe("pasta/log")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode("utf-8")))
    topics = msg.topic.split('/')
    payload = msg.payload.decode("utf-8")

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")
mqttc.loop_start()

while True:
    print("SAME SAME")
    time.sleep(1)