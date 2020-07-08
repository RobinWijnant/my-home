import logging
import os
import asyncio
import tracemalloc
from enum import Enum

import blynklib
import schedule
from dotenv import load_dotenv

import logger
from src.roller_blind import RollerBlind


class VirtualPin(Enum):
    POSITION = 10
    TOGGLE_DAILY_ROLL = 12
    DAILY_ROLL_TIME = 13


load_dotenv()
tracemalloc.start()

blynk = blynklib.Blynk(os.getenv("BLYNK_TOKEN"))
logger = logging.getLogger("blynk")
current_task = None
roller_blind = RollerBlind()
status = {
    "is_position_synced": False,
    "should_roll_daily": True,
}


async def run(coroutine, success_message):
    try:
        print(current_task)
        current_task.cancel()
    except UnboundLocalError:
        pass

    current_task = asyncio.create_task(coroutine)
    current_task.add_done_callback(lambda task: logger.info(success_message))
    await current_task


def do_daily_roll(direction_up):
    if direction_up:
        logger.info(f"Daily roll up starting...")
        asyncio.run(run(roller_blind.roll(0), "Daily roll up finished"))
        blynk.virtual_write(VirtualPin.POSITION.value, 0)
    else:
        logger.info(f"Daily roll down starting...")
        asyncio.run(run(roller_blind.roll(1000), "Daily roll down finished"))
        blynk.virtual_write(VirtualPin.POSITION.value, 1000)


def int_to_time(value):
    hours = value / 60 / 60
    minutes = value / 60 % 60
    return f"{str(int(hours)).zfill(2)}:{str(int(minutes)).zfill(2)}"


@blynk.handle_event("connect")
def handle_connect():
    logger.info(f"Pulling latest values from Blynk servers...")
    blynk.virtual_sync(VirtualPin.POSITION.value)
    blynk.virtual_sync(VirtualPin.TOGGLE_DAILY_ROLL.value)

    # recommended by blynkkk/lib-python
    # https://github.com/blynkkk/lib-python/blob/master/examples/09_sync_virtual_pin.py
    blynk.read_response(timeout=0.5)

    logger.info(f"Pulling completed")


@blynk.handle_event("write V10")
def handle_update_position(pin, value):
    if status["is_position_synced"] == False:
        roller_blind.position = int(value[0])
        status["is_position_synced"] = True
        logger.info(f"New position set ({value[0]}‰)")
        return

    logger.info(f"Setting new position ({value[0]}‰)...")
    asyncio.run(run(roller_blind.roll(int(value[0])), "New position reached"))


@blynk.handle_event("write V11")
def handle_calibrate(pin, value):
    if not int(value[0]):
        return

    logger.info("Calibrating...")
    asyncio.run(run(roller_blind.calibrate(), "Calibration completed"))
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)


@blynk.handle_event("write V12")
def handle_toggle_daily_roll(pin, value):
    if int(value[0]):
        status["should_roll_daily"] = True
        blynk.virtual_sync(VirtualPin.DAILY_ROLL_TIME.value)
        blynk.read_response(timeout=0.5)
        logger.info("Daily roll activated")

    if not int(value[0]):
        status["should_roll_daily"] = False
        schedule.clear("daily-roll")
        logger.info("Daily roll deactivated")


@blynk.handle_event("write V13")
def handle_time(pin, value):
    if not status["should_roll_daily"]:
        return
    schedule.clear("daily-roll")

    if int(value[0]):
        time = int_to_time(int(value[0]))
        schedule.every().day.at(time).do(do_daily_roll, True).tag("daily-roll")
        logger.info(f"Daily roll up set to {time}")

    if int(value[1]):
        time = int_to_time(int(value[1]))
        schedule.every().day.at(time).do(do_daily_roll, False).tag("daily-roll")
        logger.info(f"Daily roll down set to {time}")


@blynk.handle_event("disconnect")
def handle_disconnect():
    logger.info(f"Pushing latest values to Blynk servers...")
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)
    logger.info(f"Pushing completed")


try:
    asyncio.run(run(roller_blind.roll(2), "New position reached1"))
    asyncio.run(run(roller_blind.roll(4), "New position reached2"))
    while True:
        blynk.run()
        schedule.run_pending()

except KeyboardInterrupt:
    print()
    logger.warning("Script interrupted by user")

    try:
        current_task.cancel()
    except UnboundLocalError:
        pass

    blynk.disconnect()
