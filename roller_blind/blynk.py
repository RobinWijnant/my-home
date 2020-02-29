import os
import logging
import blynklib
from roller_blind.roller_blind import RollerBlind

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
roller_blind = RollerBlind()

@blynk.handle_event('write V10')
def update_position(pin, value):
    logger.info(f'Setting new position ({value[0]}%)...')
    roller_blind.roll(int(value[0]))
    logger.info('New position reached')

@blynk.handle_event('write V11')
def calibrate(pin, value):
    if (not int(value[0])): return
    logger.info('Calibrating...')
    roller_blind.calibrate()
    logger.info('Calibration completed')

while True:
    blynk.run()