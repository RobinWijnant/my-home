from roller_blind.stepper_motor import StepperMotor

STEP_MODE_PINS = (14, 15, 18)
DIRECTION_PIN= 20
STEP_PIN = 21

stepper = StepperMotor(DIRECTION_PIN, STEP_PIN, STEP_MODE_PINS)

step_mode = "1/16" # Full, Half, 1/4, 1/8, 1/16, 1/32
is_clockwise = True
steps = 10000

stepper.step_mode = step_mode
stepper.go(steps, is_clockwise)