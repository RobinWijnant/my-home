import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from roller_blind.digital_hall_sensor import DigitalHallSensor

class RollerBlind:

  STEP_MODE_PINS = (14, 15, 18)
  STEP_DIRECTION_PIN = 20
  STEP_PIN = 21
  STEP_DRIVER = "DRV8825"
  HALL_SENSOR_49E = 26

  step_type = "1/8"
  steps_to_position_100 = 360 / 1.8 * 8 * 25
  step_delay = .00001
  init_delay = .05

  def __init__(self):
    self.stepper = RpiMotorLib.A4988Nema(RollerBlind.STEP_DIRECTION_PIN, RollerBlind.STEP_PIN, RollerBlind.STEP_MODE_PINS, RollerBlind.STEP_DRIVER)
    self.hall_sensor = DigitalHallSensor(self.HALL_SENSOR_49E)
    self.position = 0 # [0,100]
    self.magnetic_strength = 0 # [0,100]
    self.calibrate()

  def calibrate(self):
    while(self.hall_sensor.detect()):
      self.stepper.motor_go(
        clockwise=False,
        steptype=self.step_type,
        steps=200,
        stepdelay=self.step_delay,
        verbose=False,
        initdelay=self.init_delay
      )
    self.position = 0

  def roll(self, position):
    if (position > self.position):
      self._roll_down(position)
    else:
      self._roll_up(position)

  def _roll_up(self, position):
    position_diff = 1
    while(position < self.position):
      self.stepper.motor_go(
        clockwise=False,
        steptype=self.step_type,
        steps=self._convert_position_diff_to_steps(position_diff),
        stepdelay=self.step_delay,
        verbose=False,
        initdelay=self.init_delay
      )
      self.position = position - position_diff

  def _roll_down(self, position):
    position_diff = 1
    while(position > self.position):
      self.stepper.motor_go(
        clockwise=True,
        steptype=self.step_type,
        steps=self._convert_position_diff_to_steps(position_diff),
        stepdelay=self.step_delay,
        verbose=False,
        initdelay=self.init_delay
      )
      self.position = self.position + position_diff

  def _convert_position_diff_to_steps(self, position_diff):
    return self.steps_to_position_100 / 100 * position_diff
