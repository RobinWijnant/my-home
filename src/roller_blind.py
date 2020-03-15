from enum import Enum

import board
from src.hall_sensor import HallSensor
from src.stepper_motor import StepperMotor


class RollDirection(Enum):
  UP = True
  DOWN = False

class RollerBlind:

  STEP_MODE_PINS = (14, 15, 18)
  STEP_DIRECTION_PIN = 23
  STEP_STEP_PIN = 24
  STEP_SLEEP_PIN = 17
  
  ROTATIONS_UNTIL_DOWN = 400

  def __init__(self):
    self.stepper = StepperMotor(RollerBlind.STEP_DIRECTION_PIN, RollerBlind.STEP_STEP_PIN, RollerBlind.STEP_MODE_PINS, RollerBlind.STEP_SLEEP_PIN)
    self.hall_sensor = HallSensor(board.SDA, board.SCL)
    self.position = 0 # [0,100]

  def calibrate(self):
    self.stepper.set_sleep(False)
    while(not self.hall_sensor.detect()):
      self.stepper.go(self._convert_position_diff_to_steps(0.1), RollDirection.UP.value)
    self.position = 0
    self.stepper.set_sleep(True)

  def roll(self, position):
    self.stepper.set_sleep(False)
    if (position > self.position):
      self._roll_down(position)
    else:
      self._roll_up(position)
    self.position = position
    self.stepper.set_sleep(True)

  def _roll_up(self, position):
    position_diff = self.position - position
    self.stepper.go(self._convert_position_diff_to_steps(position_diff), RollDirection.UP.value)
    
  def _roll_down(self, position):
    position_diff = position - self.position
    self.stepper.go(self._convert_position_diff_to_steps(position_diff), RollDirection.DOWN.value)

  def _convert_position_diff_to_steps(self, position_diff):
    steps_for_1_rotation = 360 / 1.8 * self.stepper.get_step_mode_multiplier()
    steps_to_position_100 = steps_for_1_rotation * RollerBlind.ROTATIONS_UNTIL_DOWN
    return int(steps_to_position_100 / 100 * position_diff)
