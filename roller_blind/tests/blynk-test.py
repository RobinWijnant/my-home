import blynklib
import os

WRITE_PRINT_MSG = "Slider value: {}"

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    print(WRITE_PRINT_MSG.format(value))
    
while True:
    blynk.run()