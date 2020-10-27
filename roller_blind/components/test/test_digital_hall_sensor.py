import time
import unittest

from src.components.digital_hall_sensor import DigitalHallSensor

SENSOR_PIN = 25


class StepperMotorTest(unittest.TestCase):
    def setUp(self):
        self.sensor = DigitalHallSensor(SENSOR_PIN)

    def test_listen(self):
        try:
            while True:
                print(self.sensor.detect())
                time.sleep(1)
        except KeyboardInterrupt:
            pass
