# inspired by IO-Link master with EtherNet/IP interface AL1322 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/AL1322
import paho.mqtt.client as mqtt
from datetime import datetime
import time
from sensor import *
from utils import *

IO_LINK_PORTS = 8


class Master:
    def __init__(self, name):
        self.name = name
        self.sensors = IO_LINK_PORTS * [None]
        self.sensors_measurements = IO_LINK_PORTS * [None]
        # TODO

    def add_sensor(self, sensor, port_index):
        if self.sensors[port_index] is None:
            self.sensors[port_index] = sensor
            return True
        else:
            print("ERROR - port {index} is unavailable".format(index=port_index))
            return False

    def remove_sensor(self, port_index):
        if self.sensors[port_index] is None:
            print("ERROR - port {index} is not used".format(index=port_index))
            return False
        else:
            self.sensors[port_index] = None
            return True

    def read_sensors(self):
        for index, sensor in enumerate(self.sensors):
            if sensor is not None:
                data = self.normalize(sensor.get_data())
                self.sensors_measurements[index] = data

    def normalize(self, data):
        rescaled_data = {
            "sensor_name": data["device_name"],
            "datetime": str(datetime.now()),
            "status": data["device_status"],
            "temperature": data["temperature"] * data["scale_temperature"],
            "vibration_acc_RMS": data["a_RMS"] * data["scale_a_RMS"],
            "vibration_acc_peak": data["a_peak"] * data["scale_a_peak"],
            "vibration_vel_RMS": data["v_RMS"] * data["scale_v_RMS"],
            "crest": data["crest"] * data["scale_crest"]
        }
        return rescaled_data

    '''
    MQTT message format:
    {
        "sensor_name" : String,
        "datetime" : Datetime,
        "status" : int,
        "temperature" : float,
        "vibration_acc_RMS" : float,
        "vibration_acc_peak" : float,
        "vibration_vel_RMS" : float,
        "crest" : float        
    }
    '''

    def send(self, mqttc):
        for index, measurement in enumerate(self.sensors_measurements):
            if measurement is not None:
                topic = 'pasta/master/' + self.name + '/' + str(index)
                data = dict_to_jsonstr(measurement)
                print(data)
                mqttc.publish(topic, data, 0, False)

    def run(self, mqqtc):
        mqttc.loop_start()
        while True:
            time.sleep(5)
            self.read_sensors()
            print("sending...")
            self.send(mqttc)


# test
master = Master("AL1322")
master.add_sensor(Sensor("VVB02_1"), 0)
master.add_sensor(Sensor("VVB02_2"), 1)
master.add_sensor(Sensor("VVB02_3"), 4)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

print("Master")
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.connect("test.mosquitto.org")

master.run(mqttc)

