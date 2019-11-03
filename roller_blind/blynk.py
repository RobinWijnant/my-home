import os
import blynklib

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    print(f'Slider value: {value}')
    
while True:
    blynk.run()