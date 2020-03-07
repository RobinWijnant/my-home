from enum import Enum

from roller_blind.digital_hall_sensor import DigitalHallSensor
from roller_blind.stepper_motor import StepperMotor


class RollDirection(Enum):
  UP = True
  DOWN = False

class RollerBlind:

  STEP_MODE_PINS = (14, 15, 18)
  STEP_DIRECTION_PIN = 23
  STEP_PIN = 24
  HALL_SENSOR_49E_PIN = 25

  rotations_until_down = 25

  def __init__(self):
    self.stepper = StepperMotor(RollerBlind.STEP_DIRECTION_PIN, RollerBlind.STEP_PIN, RollerBlind.STEP_MODE_PINS)
    self.hall_sensor = DigitalHallSensor(RollerBlind.HALL_SENSOR_49E_PIN)
    self.position = 0 # [0,100]

  def calibrate(self):
    while(not self.hall_sensor.detect()):
      self.stepper.go(self._convert_position_diff_to_steps(1), RollDirection.UP)
    self.position = 0

  def roll(self, position):
    if (position > self.position):
      self._roll_down(position)
    else:
      self._roll_up(position)

  def _roll_up(self, position):
    position_diff = 1
    while(position < self.position):
      self.stepper.go(self._convert_position_diff_to_steps(position_diff), RollDirection.UP)
      self.position = self.position - position_diff

  def _roll_down(self, position):
    position_diff = 1
    while(position > self.position):
      self.stepper.go(self._convert_position_diff_to_steps(position_diff), RollDirection.DOWN)
      self.position = self.position + position_diff

  def _convert_position_diff_to_steps(self, position_diff):
    steps_for_1_rotation = 360 / 1.8 * self.stepper.get_step_mode_multiplier()
    steps_to_position_100 = steps_for_1_rotation * RollerBlind.rotations_until_down
    return int(steps_to_position_100 / 100 * position_diff)
