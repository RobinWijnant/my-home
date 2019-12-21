import RPi.GPIO as gpio

class DigitalHallSensor():

    def __init__(self, pin):
        self.pin = pin
        gpio.setup(pin, gpio.IN)

    def detect(self):
        return gpio.input(self.pin)