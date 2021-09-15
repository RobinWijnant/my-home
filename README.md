# My Home

🎚 Python 3 scripts running on Raspberry Pi 4 that listen to MQTT events.

## Features

- Adjustable roller blind height
- 433Mhz listener for the doorbell button
- camera webserver

## Getting started

### Installation

The following pip packages are required:

```bash
pip3 install \
  wheel \
  adafruit-blinka \
  RPi.GPIO \
  python-dotenv \
  RpiMotorLib \
  adafruit-circuitpython-ads1x15 \
  paho-mqtt
```

> **Note:** RPi.GPIO is installed by default on a Raspberry Pi and is not installable on other devices

### Running the script

Run the scripts:

```bash
python3 src/roller_blind/main.py
python3 src/doorbell/main.py
```

## Systemd service

A service is used to easily start and stop the script. It also allows to run on startup.

To create the service in systemd, copy the service file into the system folder:

```bash
cp src/roller_blind/systemd.service /lib/systemd/system/roller_blind.service
```

Edit the environment vars

```bash
systemctl edit roller-blind
```

```env
MQTT_HOST=192.168.0.10
```

Reload the daemon to recognise the new service, then start the blynk service. Enabling the service is optional, this will make it start automatically on startup.

```bash
systemctl daemon-reload
systemctl start 'home:*'
systemctl enable 'home:*'
```

## Running test files

This project uses the unittest module to run tests. There are no additional packages needed to install.

Run all tests:

```bash
python3 -m unittest discover -s ./src/roller_blind/components/test
```

Run a single test

```bash
python3 -m unittest src.roller_blind.components.test.test_stepper_motor
```
