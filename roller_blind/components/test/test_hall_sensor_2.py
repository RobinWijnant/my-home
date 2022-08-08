import time
import unittest

import RPi.GPIO as GPIO

time.sleep(0.5)

PIN = 26

class HallSensorTest(unittest.TestCase):
    def setUp(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN)

    def test_read_strength(self):
        try:
            while True:
                print(GPIO.input(PIN))
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass
