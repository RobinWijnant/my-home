from RpiMotorLib import RpiMotorLib

import RPi.GPIO as GPIO


class StepperMotor:

  DRIVER = "DRV8825"
  INIT_DELAY = 0

  def __init__(self, direction_pin, step_pin, mode_pins, sleep_pin):
    self.step_mode = "1/8"
    self.stepper = RpiMotorLib.A4988Nema(direction_pin, step_pin, mode_pins, StepperMotor.DRIVER)
    self.sleep_pin = sleep_pin
    GPIO.output(self.sleep_pin, GPIO.LOW)

  def go(self, steps, is_clockwise):
    GPIO.output(self.sleep_pin, GPIO.HIGH)
    self.stepper.motor_go(
      clockwise=is_clockwise,
      steptype=self.step_mode,
      steps=steps,
      stepdelay=self._get_step_delay(),
      verbose=False,
      initdelay=StepperMotor.INIT_DELAY
    )
    GPIO.output(self.sleep_pin, GPIO.LOW)

  def _get_step_delay(self):
    if (self.step_mode == "1/32"):
      return 0.0001
    if (self.step_mode == "1/16"):
      return 0.0001
    if (self.step_mode == "1/8"):
      return 0.0001
    if (self.step_mode == "1/4"):
      return 0.0001
    if (self.step_mode == "Half"):
      return 0.001
    return 0.01

  def get_step_mode_multiplier(self):
    if (self.step_mode == "1/32"):
      return 32
    if (self.step_mode == "1/16"):
      return 16
    if (self.step_mode == "1/8"):
      return 8
    if (self.step_mode == "1/4"):
      return 4
    if (self.step_mode == "Half"):
      return 2
    return 1
