import RPi.GPIO as GPIO


class DigitalHallSensor:

    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)

    def detect(self):
        return not GPIO.input(self.pin)
