import os
import logging
import blynklib
from roller_blind import RollerBlind

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
roller_blind = RollerBlind()

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    logger.info(f'Set new position: {value}%')
    roller_blind.roll(value)

while True:
    blynk.run()