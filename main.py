import logging
import os
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

import blynklib
import schedule
from dotenv import load_dotenv

import logger
from src.roller_blind import RollerBlind


class VirtualPin(Enum):
    POSITION = 10

load_dotenv()

blynk = blynklib.Blynk(os.getenv('BLYNK_TOKEN'))
logger = logging.getLogger('blynk')
executor = ThreadPoolExecutor(max_workers=1)
roller_blind = RollerBlind()

has_synced = {
    VirtualPin.POSITION.value: False,
}

def do_daily_roll(direction_up):
    if (direction_up):
        logger.info(f'Daily roll up starting...')
        future = executor.submit(roller_blind.roll, 0)
        future.add_done_callback(lambda future: logger.info('Daily roll up finished'))
    logger.info(f'Daily roll down starting...')
    future = executor.submit(roller_blind.roll, 100)
    future.add_done_callback(lambda future: logger.info('Daily roll down finished'))

def int_to_time(value):
    hours = value / 60 / 60
    minutes = value / 60 % 60
    print(f'{int(hours)}:{int(minutes)}')
    return f'{int(hours)}:{int(minutes)}'


@blynk.handle_event("connect")
def handle_connect():
    logger.info(f'Pulling latest values from Blynk servers...')
    blynk.virtual_sync(10)
    blynk.virtual_sync(13)

    # recommended by blynkkk/lib-python
    # https://github.com/blynkkk/lib-python/blob/master/examples/09_sync_virtual_pin.py
    blynk.read_response(timeout=0.5) 

    logger.info(f'Pulling completed')


@blynk.handle_event('write V10')
def handle_update_position(pin, value):
    if (has_synced[VirtualPin.POSITION.value] == False):
        roller_blind.position = int(value[0])
        has_synced[VirtualPin.POSITION.value] = True
        logger.info(f'New position set ({value[0]}%)')
        return

    logger.info(f'Setting new position ({value[0]}%)...')
    future = executor.submit(roller_blind.roll, int(value[0]))
    future.add_done_callback(lambda future: logger.info('New position reached'))

@blynk.handle_event('write V11')
def handle_calibrate(pin, value):
    if (not int(value[0])): return

    logger.info('Calibrating...')
    future = executor.submit(roller_blind.calibrate)
    future.add_done_callback(lambda future: logger.info('Calibration completed'))
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)

@blynk.handle_event('write V13')
def handle_time(pin, value):
    schedule.clear('daily-roll')
    print(int(value[0]))
    if (int(value[0])):
        schedule.every().day.at(int_to_time(int(value[0]))).do(do_daily_roll, True).tag('daily-roll')
    print(int(value[1]))
    if (int(value[1])):
        schedule.every().day.at(int_to_time(int(value[1]))).do(do_daily_roll, False).tag('daily-roll')

@blynk.handle_event("disconnect")
def handle_disconnect():
    logger.info(f'Pushing latest values to Blynk servers...')
    blynk.virtual_write(VirtualPin.POSITION.value, roller_blind.position)
    logger.info(f'Pushing completed')

try:
    while True:
        blynk.run()
        schedule.run_pending()

except KeyboardInterrupt:
    print()
    executor.shutdown()
    blynk.disconnect()
    logger.warning('Script interrupted by user')
