import logging
import os
import json
import sys
import time
import paho.mqtt.client as mqtt

from dotenv import load_dotenv

sys.path.append("../packages")
import ha_config
import common.logger
from common.thread_manager import ThreadManager
from radio_switch import RadioSwitch

load_dotenv()

logger = logging.getLogger("home")
client = mqtt.Client()
topic = f"{os.getenv('MQTT_PREFIX')}/device_automation/{os.getenv('DEVICE_ID')}"
r_switch = RadioSwitch()
thread_manager = ThreadManager()


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connection established with MQTT broker")
    main_config = ha_config.get_main_button_config(topic)
    client.publish(f"{topic}/config", json.dumps(main_config))
    thread_manager.execute(listen_click)


def listen_click(stopped):
    logger.info(f"Listening to doorbell button...")
    while True:
        if stopped():
            break
        if r_switch.is_available():
            message = r_switch.read()
            logger.info(f"New button press {json.dumps(message)}")
            # 15475652 15475650
        time.sleep(0.01)


try:
    logger.info(f"Connecting to MQTT broker...")
    client.enable_logger(logger=logger)
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    client.on_connect = on_connect
    client.connect(os.getenv("MQTT_HOST"))
    client.loop_forever()

except KeyboardInterrupt:
    print()
    thread_manager.stop()
    client.disconnect()
    logger.warning("Script interrupted by user")
