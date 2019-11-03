import logging

logger = logging.getLogger('blynk')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s]: %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler('blynk.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)-15s [%(levelname)s]: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)