# My Home

🎚 A python 3 script running on Raspberry Pi 4 that runs on MQTT events.

## Features

- Adjustable roller blind height
- 433Mhz listener for the doorbell button

## Getting started

### Installation

When running on an alpine image, install these packages:

```bash
apk add \
  gcc \
  python3-dev \
  musl-dev \
  linux-headers
```

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

### Environment

Create a .env file in the root of the repository and set these variables:

```env
MQTT_HOST=192.168.0.10
```

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
cp src/doorbell/systemd.service /lib/systemd/system/doorbell.service
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
