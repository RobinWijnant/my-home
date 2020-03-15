import time
import unittest

import board
from src.hall_sensor import HallSensor

time.sleep(0.5)

class HallSensorTest(unittest.TestCase):

    def setUp(self):
        self.sensor = HallSensor(board.scl, board.sda)

    def test_read_strength(self):
        try:
            while True:
                print(self.sensor.read_strength())
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
