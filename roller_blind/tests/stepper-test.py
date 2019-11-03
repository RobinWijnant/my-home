import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#GPIO pins
STEP_MODE_PINS = (14, 15, 18)
DIRECTION_PIN= 20
STEP_PIN = 21

stepper = RpiMotorLib.A4988Nema(DIRECTION_PIN, STEP_PIN, STEP_MODE_PINS, "DRV8825")

isClockwise = True
stepMode = "1/16" # Full, Half, 1/4, 1/8, 1/16, 1/32
steps = 10000

stepper.motor_go(isClockwise, stepMode, steps, .001, False, .005)

GPIO.cleanup()