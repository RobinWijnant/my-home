import logging
import os
import json
import sys
import paho.mqtt.client as mqtt

from dotenv import load_dotenv

sys.path.append("../packages")
import ha_config
import common.logger

load_dotenv()

logger = logging.getLogger("home")
client = mqtt.Client()
topic = f"{os.getenv('MQTT_PREFIX')}/device_automation/{os.getenv('DEVICE_ID')}"


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connection established with MQTT broker")
    main_config = ha_config.get_main_button_config(topic)
    client.publish(f"{topic}/config", json.dumps(main_config))


try:
    logger.info(f"Connecting to MQTT broker...")
    client.enable_logger(logger=logger)
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    client.on_connect = on_connect
    client.connect(os.getenv("MQTT_HOST"))
    client.loop_forever()

except KeyboardInterrupt:
    print()
    client.disconnect()
    logger.warning("Script interrupted by user")
