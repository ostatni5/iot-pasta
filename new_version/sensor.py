#!/usr/bin/python
# -*- coding: utf-8 -*-

# inspired by vibration sensor VVB021 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/VVB021

# device statuses:
from time import sleep

DEVICE_OK = 0
MAINTENANCE_REQUIRED = 1
OUT_OF_SPECIFICATION = 2
FUNCTIONAL_CHECK = 3
FAILURE = 4

# all measurements will be scaled properly in master, now they`re send using integer values
# scale S represents power of 10 by which measurement will be divided by
# temperature - measurement step and range:
TEMP_MAX = 800  # measurement in degrees Celsius - °C
TEMP_MIN = -300  # [°C]
TEMP_SCALE = -1
# will be scaled by 0.1

# vibration acceleration RMS - measurement step and range:
VIB_ACC_RMS_MAX = 4903  # measurement in m/s^2
VIB_ACC_RMS_MIN = 0  # [m/s^2]
VIB_ACC_RMS_SCALE = -1
# will be scaled 0.1

# vibration acceleration peak - measurement step and range:
VIB_ACC_PEAK_MAX = 4903  # measurement in m/s^2
VIB_ACC_PEAK_MIN = 0  # [m/s^2]
VIB_ACC_PEAK_SCALE = -1
# will be scaled by 0.1

# vibration velocity - measurement step and range:
VIB_VEL_MAX = 495  # measurement in meters per second
VIB_VEL_MIN = 0  # [m/s]
VIB_VEL_SCALE = -4
# will be scaled by 0.0001

# crest
CREST_MAX = 500
CREST_MIN = 10
CREST_SCALE = -1
# will be scaled by 0.1

# if there is no data, sensor sends NoData flag
NO_DATA = 32764


class Sensor:
    def __init__(self, name, master, delay):
        self.name = name
        self.master = master
        self.status = DEVICE_OK
        self.delay = delay
        self.parameters = {
            "temperature": 0,
            "vibration_acc": 0,
            "vibration_vel": 0
        }
        self.running = False

    def run(self):
        self.running = True
        # TODO - wait, measure, send
        while self.running:
            sleep(self.delay)
            self.measure()
            self.send()

    def measure(self):
        # TODO update measuremenets somehow
        pass

    def send(self):
        # TODO wysłać dane do mastera, sposob ze strony 10
        pass

    def stop(self):
        self.running = False
