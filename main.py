import logging
import os
from enum import Enum

import blynklib
from dotenv import load_dotenv

import logger
from src.roller_blind import RollerBlind


class VirtualPin(Enum):
    POSITION = 10

load_dotenv()
blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
roller_blind = RollerBlind()
has_synced = {
    VirtualPin.POSITION.value: False,
}

@blynk.handle_event("connect")
def handle_connect():
    logger.info(f'Pulling latest values from Blynk servers...')
    blynk.virtual_sync(10)

    # recommended by blynkkk/lib-python
    # https://github.com/blynkkk/lib-python/blob/master/examples/09_sync_virtual_pin.py
    blynk.read_response(timeout=0.5) 

    logger.info(f'Pulling completed')


@blynk.handle_event('write V10')
def handle_update_position(pin, value):
    if (has_synced[VirtualPin.POSITION.value] == False):
        roller_blind.position = value
        has_synced[VirtualPin.POSITION.value] = True
        return

    logger.info(f'Setting new position ({value[0]}%)...')
    roller_blind.roll(int(value[0]))
    logger.info('New position reached')

@blynk.handle_event('write V11')
def handle_calibrate(pin, value):
    if (not int(value[0])): return

    logger.info('Calibrating...')
    roller_blind.calibrate()
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)
    logger.info('Calibration completed')

@blynk.handle_event("disconnect")
def handle_disconnect():
    logger.info(f'Pushing latest values to Blynk servers...')
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)
    logger.info(f'Pushing completed')

try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    print('Script interrupted by user')
