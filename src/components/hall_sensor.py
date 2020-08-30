import math

import adafruit_ads1x15.ads1015 as ADS
import busio
from adafruit_ads1x15.analog_in import AnalogIn


class HallSensor:
    def __init__(self, scl_pin, sda_pin):
        i2c = busio.I2C(scl_pin, sda_pin)
        ads = ADS.ADS1015(i2c)
        self.channel = AnalogIn(ads, ADS.P0)

    def read_strength(self):
        return self.channel.value / math.pow(2, 16) * 100  # [0,100]

    def detect(self):
        value = self.read_strength()
        return value > 15
