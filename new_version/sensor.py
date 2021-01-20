#!/usr/bin/python
# -*- coding: utf-8 -*-
# inspired by vibration sensor VVB021 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/VVB021

# temperature measurement step and range
TEMP_MAX = 80  # measurement in degrees Celsius - °C
TEMP_STEP = 0.1  # measurement accuracy
TEMP_MIN = -30  # [°C]

# vibration acceleration measurement step and range
VIB_ACC_MAX = 50  # measurement in g's - Earth`s gravitational acceleration = 9,81 m/s^2
VIB_ACC_STEP = 0.2  # measurement accuracy
VIB_ACC_MIN = 0

# vibration velocity measurement step and range
VIB_VEL_MAX = 45  # measurement in milimeters per second
VIB_VEL_STEP = 0.2  # measurement resolution/precision
VIB_VEL_MIN = 0  # [mm/s]


class Sensor:
    def __init__(self, name):
        self.name = name
        # TODO

