import math
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class HallSensor():

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS.ADS1115(i2c)
        self.channel = AnalogIn(ads, ADS.P0)

    def read_strength(self):
        return self.channel.value / math.pow(2, 16) * 100