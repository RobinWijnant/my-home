import logging
import os
import paho.mqtt.client as mqtt
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from dotenv import load_dotenv

import src.logger
from .roller_blind import RollerBlind
from ..stoppable_thread import StoppableThread

load_dotenv()

logger = logging.getLogger("home")
roller_blind = RollerBlind()
client = mqtt.Client()
current_thread = None
is_position_synced = False
topic = "roller_blind"


def thread(*args, **kwargs):
    global current_thread
    if current_thread is not None:
        current_thread.stop()
        current_thread.join()

    current_thread = StoppableThread(*args, **kwargs)
    current_thread.start()


def update_position(value):
    logger.info(f"Rolling from {roller_blind.position}‰ to position {value}‰...")

    def on_complete():
        mqtt.publish(f"{topic}/stop", value)
        logger.info(f"Roll completed to {value}‰")

    thread(roller_blind.roll, value, on_complete=on_complete)


def calibrate():
    logger.info("Calibrating...")

    def on_complete():
        mqtt.publish(f"{topic}/stop", 0)
        logger.info("Calibration completed")

    thread(roller_blind.calibrate, on_complete=on_complete)


def interrupt():
    logger.warning(f"Stopping motor...")
    if current_thread is not None:
        current_thread.stop()
        current_thread.join()
    mqtt.publish(f"{topic}/stop", roller_blind.position)
    logger.warning(f"Motor stopped")


def on_connect():
    logger.info(f"Connection established with MQTT broker")
    mqtt.subscribe(f"{topic}/#")
    mqtt.publish(f"{topic}/calibrate", 0)


def on_message(client, userdata, message):
    if message.topic is f"{topic}/calibrate":
        calibrate()
    elif message.topic is f"{topic}/start":
        update_position(int(message.payload))
    elif message.topic is f"{topic}/force_stop":
        interrupt()


try:
    logger.info(f"Connecting to MQTT broker...")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(os.getenv("MQTT_HOST"))
    client.loop_forever()

except KeyboardInterrupt:
    print()

    if current_thread is not None:
        current_thread.stop()
        current_thread.join()

    client.disconnect()
    logger.warning("Script interrupted by user")
