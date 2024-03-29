from RpiMotorLib import RpiMotorLib

import RPi.GPIO as GPIO


class StepperMotor:

  DRIVER = "DRV8825"
  INIT_DELAY = 0

  def __init__(self, direction_pin, step_pin, mode_pins, sleep_pin):
    self.step_mode = "1/16"
    self.stepper = RpiMotorLib.A4988Nema(direction_pin, step_pin, mode_pins, StepperMotor.DRIVER)
    self.sleep_pin = sleep_pin
    GPIO.setup(self.sleep_pin, GPIO.OUT)
    self.set_sleep(True)

  def set_sleep(self, is_sleep):
    if (is_sleep):
      GPIO.output(self.sleep_pin, GPIO.LOW)
    else:
      GPIO.output(self.sleep_pin, GPIO.HIGH)

  def go(self, steps, is_clockwise):
    self.stepper.motor_go(
      clockwise=is_clockwise,
      steptype=self.step_mode,
      steps=steps,
      stepdelay=self._get_step_delay(),
      verbose=False,
      initdelay=StepperMotor.INIT_DELAY
    )

  def _get_step_delay(self):
    if (self.step_mode == "1/32"):
      return 0.000000000000001
    if (self.step_mode == "1/16"):
      return 0.000000000000001
    if (self.step_mode == "1/8"):
      return 0.000000001
    if (self.step_mode == "1/4"):
      return 0.000004
    if (self.step_mode == "Half"):
      return 0.00002
    return 0.0005

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
