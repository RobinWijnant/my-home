import asyncio
from enum import Enum

import board
from src.digital_hall_sensor import DigitalHallSensor
from src.stepper_motor import StepperMotor


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
        self.position = 0  # [0,1000]

    async def calibrate(self):
        self.stepper.set_sleep(False)
        while not self.hall_sensor.detect():
            await self.stepper.go(
                self._convert_position_diff_to_steps(1), RollDirection.UP.value
            )
        self.position = 0
        self.stepper.set_sleep(True)

    async def roll(self, position):
        self.stepper.set_sleep(False)
        if position > self.position:
            await self._roll_down(position)
        else:
            await self._roll_up(position)
        self.stepper.set_sleep(True)

    async def _roll_up(self, position):
        position_diff = self.position - position
        for incrementing_position in range(position_diff):
            try:
                await self.stepper.go(
                    self._convert_position_diff_to_steps(incrementing_position),
                    RollDirection.UP.value,
                )
                self.position = incrementing_position
            except asyncio.CancelledError:
                return

    async def _roll_down(self, position):
        position_diff = position - self.position
        print(position, self.position, position_diff)
        for incrementing_position in range(position_diff):
            try:
                await self.stepper.go(
                    self._convert_position_diff_to_steps(incrementing_position),
                    RollDirection.DOWN.value,
                )
                self.position = incrementing_position
            except asyncio.CancelledError:
                return

    def _convert_position_diff_to_steps(self, position_diff):
        steps_for_1_rotation = 360 / 1.8 * self.stepper.get_step_mode_multiplier()
        steps_until_down = steps_for_1_rotation * RollerBlind.ROTATIONS_UNTIL_DOWN
        return int(steps_until_down / 1000 * position_diff)

