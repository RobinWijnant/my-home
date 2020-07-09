import time
import unittest

import board
from src.hall_sensor import HallSensor

time.sleep(0.5)

class HallSensorTest(unittest.TestCase):

    def setUp(self):
        self.sensor = HallSensor(board.SCL, board.SDA)

    def test_detect(self):
        try:
            while True:
                print(self.sensor.detect())
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
