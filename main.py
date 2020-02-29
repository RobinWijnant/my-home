from dotenv import load_dotenv
load_dotenv()

import logger

try:
    import roller_blind.blynk
except KeyboardInterrupt:
    print()