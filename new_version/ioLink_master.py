#!/usr/bin/python
# -*- coding: utf-8 -*-

# inspired by IO-Link master with EtherNet/IP interface AL1322 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/AL1322
from datetime import datetime

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
            "datetime": datetime.now(),
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

    def send(self):
        for index, measurement in enumerate(self.sensors_measurements):
            # TODO mqttc.publish("pasta/master/id_mastera/id_portu", json(measurement) ...)
            pass
