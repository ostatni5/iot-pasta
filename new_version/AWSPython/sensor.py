# inspired by vibration sensor VVB021 made by ifm electronic gmbh
# https://www.ifm.com/de/en/product/VVB021
import math
import random
from utils import *
from generator import *

# device statuses:
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
    def __init__(self, name):
        self.name = name
        self.status = DEVICE_OK
        self.parameters = {
            "temperature": 0,
            "vibration_acc_RMS": 0,
            "vibration_acc_peak": 0,
            "vibration_vel_RMS": 0,
            "crest": 0
        }
        self.time = 0

    def measure(self):
        self.time += MEASURE_TIME
        t = self.time

        s_f = s # deviation function
        v_f = lambda x: v(s_f, x)
        a_f = lambda x: a(v_f, x)

        t_s = t-MEASURE_TIME
        vrms = rms(v_f, t_s, t)
        arms = rms(a_f, t_s, t)
        apeak = peak(a_f, t_s, t)
        crest = apeak / arms

        self.parameters["temperature"] = random.randint(0, 40)
        self.parameters["vibration_acc_RMS"] = arms
        self.parameters["vibration_acc_peak"] = apeak
        self.parameters["vibration_vel_RMS"] = vrms
        self.parameters["crest"] = crest

        # self.parameters["temperature"] = 20 * math.sin(t)
        # self.parameters["vibration_acc_RMS"] = 0.1 * math.cos(t)
        # self.parameters["vibration_acc_peak"] = 0.1 * math.cos(t)
        # self.parameters["vibration_vel_RMS"] = 0.1 * math.cos(t)
        # self.parameters["crest"] = self.parameters["vibration_acc_peak"] / self.parameters["vibration_acc_RMS"]

    def get_data(self):
        self.measure()
        return {
            "v_RMS": self.parameters["vibration_vel_RMS"],
            "scale_v_RMS": VIB_VEL_SCALE,
            "a_peak": self.parameters["vibration_acc_peak"],
            "scale_a_peak": VIB_ACC_PEAK_SCALE,
            "a_RMS": self.parameters["vibration_acc_RMS"],
            "scale_a_RMS": VIB_ACC_RMS_SCALE,
            "temperature": self.parameters["temperature"],
            "scale_temperature": TEMP_SCALE,
            "crest": self.parameters["crest"],
            "scale_crest": CREST_SCALE,
            "device_status": self.status,
            "device_name": self.name
        }
