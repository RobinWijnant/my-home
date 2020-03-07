import time
import unittest

from src.digital_hall_sensor import DigitalHallSensor

SENSOR_PIN = 25

class StepperMotorTest(unittest.TestCase):

    def setUp(self):
        self.sensor = DigitalHallSensor(SENSOR_PIN)

    def test_listen(self):
        while True:
            print(self.sensor.detect())
            time.sleep(1)
