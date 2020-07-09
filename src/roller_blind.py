from enum import Enum

import sys
import board
from src.components.digital_hall_sensor import DigitalHallSensor
from src.components.stepper_motor import StepperMotor


class RollDirection(Enum):
    UP = True
    DOWN = False


class RollerBlind:

    STEP_MODE_PINS = (14, 15, 18)
    STEP_DIRECTION_PIN = 23
    STEP_STEP_PIN = 24
    STEP_SLEEP_PIN = 17

    ROTATIONS_UNTIL_DOWN = 440

    def __init__(self):
        self.stepper = StepperMotor(
            RollerBlind.STEP_DIRECTION_PIN,
            RollerBlind.STEP_STEP_PIN,
            RollerBlind.STEP_MODE_PINS,
            RollerBlind.STEP_SLEEP_PIN,
        )
        self.hall_sensor = DigitalHallSensor(10)
        self.position = 0  # [0,100]

    def calibrate(self):
        self.stepper.set_sleep(False)
        while not self.hall_sensor.detect():
            self.stepper.go(
                self._convert_position_diff_to_steps(0.1), RollDirection.UP.value
            )
        self.position = 0
        self.stepper.set_sleep(True)

    def roll(self, position, stopped):
        self.stepper.set_sleep(False)
        if position > self.position:
            self._roll_down(position, stopped)
        else:
            self._roll_up(position, stopped)
        self.position = position
        self.stepper.set_sleep(True)

    def _roll_up(self, position, stopped):
        position_diff = self.position - position
        for incrementing_position in range(position_diff):
            print("UP", incrementing_position)
            if stopped():
                print("stop going up")
                return
            self.stepper.go(
                self._convert_position_diff_to_steps(incrementing_position),
                RollDirection.UP.value,
            )

    def _roll_down(self, position, stopped):
        position_diff = position - self.position
        for incrementing_position in range(position_diff):
            print("DOWN", incrementing_position)
            if stopped():
                print("stop going down")
                return
            self.stepper.go(
                self._convert_position_diff_to_steps(incrementing_position),
                RollDirection.DOWN.value,
            )
            self.position = incrementing_position

    def _convert_position_diff_to_steps(self, position_diff):
        steps_for_1_rotation = 360 / 1.8 * self.stepper.get_step_mode_multiplier()
        steps_to_position_100 = steps_for_1_rotation * RollerBlind.ROTATIONS_UNTIL_DOWN
        return int(steps_to_position_100 / 100 * position_diff)
