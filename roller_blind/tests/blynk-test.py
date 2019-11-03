import blynklib

BLYNK_AUTH = 'ogj-hSNL136Sryg7fbWCG6fprPYf1CLy'
WRITE_PRINT_MSG = "Slider value: {}"

blynk = blynklib.Blynk(BLYNK_AUTH)

@blynk.handle_event('write V10')
def write_virtual_pin_handler(pin, value):
    print(WRITE_PRINT_MSG.format(value))
    
while True:
    blynk.run()