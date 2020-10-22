import logging
import os
import json
import paho.mqtt.client as mqtt
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from dotenv import load_dotenv

from roller_blind.ha_config import getConfig
import common.logger
from roller_blind.roller_blind import RollerBlind
from common.stoppable_thread import StoppableThread

load_dotenv()

logger = logging.getLogger("home")
roller_blind = RollerBlind()
client = mqtt.Client()
current_thread = None
topic = f"{os.getenv('MQTT_PREFIX')}/cover/{os.getenv('DEVICE_ID')}"


def thread(*args, **kwargs):
    global current_thread
    if current_thread is not None:
        current_thread.stop()

    current_thread = StoppableThread(*args, **kwargs)
    current_thread.start()


def update_position(value):
    logger.info(f"Rolling from {roller_blind.position}‰ to position {value}‰...")

    def on_complete():
        client.publish(f"{topic}/position", roller_blind.position)
        logger.info(f"Roll completed to {roller_blind.position}‰")

    thread(roller_blind.roll, value, on_complete=on_complete)


def calibrate():
    logger.info("Calibrating...")

    def on_complete():
        client.publish(f"{topic}/position", 0)
        logger.info("Calibration completed")

    thread(roller_blind.calibrate, on_complete=on_complete)


def interrupt():
    logger.warning(f"Stopping motor...")
    if current_thread is not None:
        current_thread.stop()
        print("stop done")
    print(type(111), type(roller_blind.position), roller_blind.position)
    client.publish(f"{topic}/position", roller_blind.position)
    logger.warning(f"Motor stopped")


def on_connect(client, userdata, flags, rc):
    logger.info(f"Connection established with MQTT broker")
    config = getConfig(topic)
    client.publish(f"{topic}/config", json.dumps(config))
    client.will_set(f"{topic}/availability", "offline")
    client.publish(f"{topic}/availability", "online")
    client.subscribe(f"{topic}/#")
    client.publish(f"{topic}/calibrate", 0)


def on_message(client, userdata, message):
    if message.topic == f"{topic}/calibrate":
        calibrate()
    elif message.topic == f"{topic}/set":
        if message.payload == "OPEN":
            update_position(0)
        elif message.payload == "CLOSE":
            update_position(1000)
        else:
            interrupt()
    elif message.topic == f"{topic}/set_position":
        update_position(int(message.payload))


try:
    logger.info(f"Connecting to MQTT broker...")
    client.enable_logger(logger=logger)
    client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_HOST"))
    client.loop_forever()

except KeyboardInterrupt:
    print()

    if current_thread is not None:
        current_thread.stop()

    client.disconnect()
    logger.warning("Script interrupted by user")
