import time
from roller_blind.digital_hall_sensor import DigitalHallSensor

SENSOR_PIN = 26
sensor = DigitalHallSensor(SENSOR_PIN)

while True:
    print(sensor.detect())
    time.sleep(1)