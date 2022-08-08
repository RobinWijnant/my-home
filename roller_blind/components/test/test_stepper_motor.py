import time
import unittest

from components.stepper_motor import StepperMotor

STEP_MODE_PINS = (14, 15, 18)
DIRECTION_PIN = 23
STEP_PIN = 24
SLEEP_PIN = 17


class StepperMotorTest(unittest.TestCase):
    def setUp(self):
        self.stepper = StepperMotor(DIRECTION_PIN, STEP_PIN, STEP_MODE_PINS, SLEEP_PIN)

    def tearDown(self):
        time.sleep(1)

    def test_stepper_clockwise(self):
        step_mode = "1/16"  # Full, Half, 1/4, 1/8, 1/16, 1/32
        is_clockwise = True
        steps = 10000

        self.stepper.set_sleep(False)
        self.stepper.step_mode = step_mode
        self.stepper.go(steps, is_clockwise)
        self.stepper.set_sleep(True)
