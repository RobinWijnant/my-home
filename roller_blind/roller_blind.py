from enum import Enum

import sys
import board
from components.stepper_motor import StepperMotor


class RollDirection(Enum):
    UP = True
    DOWN = False


class RollerBlind:

    STEP_MODE_PINS = (14, 15, 18)
    STEP_DIRECTION_PIN = 23
    STEP_STEP_PIN = 24
    STEP_SLEEP_PIN = 17

    ROTATIONS_UNTIL_DOWN = 444

    def __init__(self):
        self.stepper = StepperMotor(
            RollerBlind.STEP_DIRECTION_PIN,
            RollerBlind.STEP_STEP_PIN,
            RollerBlind.STEP_MODE_PINS,
            RollerBlind.STEP_SLEEP_PIN,
        )
        self.position = 0  # [0,1000]
        self.steps_for_1_position = self._convert_position_diff_to_steps(1)

    def override_position(self, position, stopped):
        self.position = position

    def roll(self, position, stopped):
        self.stepper.set_sleep(False)

        position_diff = position - self.position
        roll_direction = RollDirection.DOWN
        if position_diff < 0:
            position_diff = abs(position_diff)
            roll_direction = RollDirection.UP

        for index in range(position_diff):
            if stopped():
                break
            self.stepper.go(
                self.steps_for_1_position,
                roll_direction.value,
            )
            self.position = (
                self.position + 1
                if roll_direction == RollDirection.DOWN
                else self.position - 1
            )

        self.stepper.set_sleep(True)

    def _convert_position_diff_to_steps(self, position_diff):
        steps_for_1_rotation = 360 / 1.8 * self.stepper.get_step_mode_multiplier()
        steps_until_down = steps_for_1_rotation * RollerBlind.ROTATIONS_UNTIL_DOWN
        return int((steps_until_down * position_diff) / 1000)
