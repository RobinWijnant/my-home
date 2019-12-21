import os
import logging
import blynklib
from roller_blind.roller_blind import RollerBlind

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
roller_blind = RollerBlind()

@blynk.handle_event('write V10')
def update_position(pin, value):
    logger.info(f'Set new position: {value[0]}%')
    roller_blind.roll(value[0])

@blynk.handle_event('write V11')
def calibrate(pin, value):
    if (value[0] == 0): return
    logger.info(f'Calibrate: {value}%')

while True:
    blynk.run()