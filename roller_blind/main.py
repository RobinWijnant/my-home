import logging
import os
import json
import sys
import paho.mqtt.client as mqtt

from dotenv import load_dotenv

sys.path.append("../packages")
import common.logger
import ha_config as ha
from roller_blind import RollerBlind
from common.thread_manager import ThreadManager

load_dotenv()

logger = logging.getLogger("home")
roller_blind = RollerBlind()
client = mqtt.Client()
thread_manager = ThreadManager()
blind_topic = f"{os.getenv('MQTT_PREFIX')}/cover/{os.getenv('DEVICE_ID')}"
calibration_open_topic = f"{os.getenv('MQTT_PREFIX')}/device_automation/{os.getenv('DEVICE_ID')}_calibration_open"
calibration_closed_topic = f"{os.getenv('MQTT_PREFIX')}/device_automation/{os.getenv('DEVICE_ID')}_calibration_closed"


def roll(value):
    logger.info(f"Rolling from {roller_blind.position}‰ to position {value}‰...")

    def on_complete():
        client.publish(f"{blind_topic}/position", roller_blind.position, retain=True)
        logger.info(f"Roll completed to {roller_blind.position}‰")

    thread_manager.execute(roller_blind.roll, value, on_complete=on_complete)


def calibrate(value):
    logger.info(f"Overriding postion {value}‰...")

    def on_complete():
        client.publish(f"{blind_topic}/position", value, retain=True)
        logger.info("Calibration completed")

    thread_manager.stop()
    thread_manager.execute(roller_blind.override_position, on_complete=on_complete)


def interrupt():
    logger.warning(f"Stopping motor...")
    thread_manager.stop()
    client.publish(f"{blind_topic}/position", roller_blind.position, retain=True)
    logger.warning(f"Motor stopped at {roller_blind.position}")


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connection established with MQTT broker")

    config = ha.get_blind_config(blind_topic)
    client.publish(f"{blind_topic}/config", json.dumps(config), retain=True)
    client.will_set(f"{blind_topic}/availability", "offline", retain=True)
    client.publish(f"{blind_topic}/availability", "online", retain=True)
    client.subscribe(f"{blind_topic}/#")

    config = ha.get_calibration_open_button_config(calibration_open_topic)
    client.publish(f"{calibration_open_topic}/config", json.dumps(config), retain=True)
    client.subscribe(f"{calibration_open_topic}/#")

    config = ha.get_calibration_closed_button_config(calibration_closed_topic)
    client.publish(
        f"{calibration_closed_topic}/config", json.dumps(config), retain=True
    )
    client.subscribe(f"{calibration_closed_topic}/#")


def on_message(client, userdata, message):
    if message.topic == f"{calibration_open_topic}/set":
        calibrate(0)
    elif message.topic == f"{calibration_closed_topic}/set":
        calibrate(1000)
    elif message.topic == f"{blind_topic}/set":
        if str(message.payload, "utf-8") == "OPEN":
            roll(0)
        elif str(message.payload, "utf-8") == "CLOSE":
            roll(1000)
        else:
            interrupt()


try:
    logger.info(f"Connecting to MQTT broker...")
    # client.enable_logger(logger=logger)
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_HOST"))
    client.loop_forever()

except KeyboardInterrupt:
    print()
    thread_manager.stop()
    client.disconnect()
    logger.warning("Script interrupted by user")
