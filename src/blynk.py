import logging
import os

import blynklib

from src.roller_blind import RollerBlind

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
roller_blind = RollerBlind()

@blynk.handle_event('write V10')
def handle_update_position(pin, value):
    logger.info(f'Setting new position ({value[0]}%)...')
    roller_blind.roll(int(value[0]))
    logger.info('New position reached')

@blynk.handle_event('write V11')
def handle_calibrate(pin, value):
    if (not int(value[0])): return
    logger.info('Calibrating...')
    roller_blind.calibrate()
    blynk.virtual_write('V10', roller_blind.position)
    logger.info('Calibration completed')

while True:
    blynk.run()
