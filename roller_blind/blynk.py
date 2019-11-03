import os
import logging
import blynklib

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    logger.INFO(f'New slider value: {value}')
    
while True:
    blynk.run()