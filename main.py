from dotenv import load_dotenv

import logger

load_dotenv()


try:
    import src.blynk
except KeyboardInterrupt:
    print()
