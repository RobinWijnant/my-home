import logging

logger = logging.getLogger("home")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(levelname)s]: %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
