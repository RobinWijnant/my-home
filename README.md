# My Home

🎚 A python 3 script running on Raspberry Pi 4 that exposes handlers for Blynk.

## Features

- Roller blind doing an up/downwards motion based on:
  - a fixed position
  - a fixed time

## Getting started

### Installation

The following pip packages are required:

```bash
pip3 install \
  python-dotenv \
  blynklib \
  RpiMotorLib \
  RPi.GPIO \
  schedule \
  adafruit_ads1x15 \
  busio
```

> **Note:** RPi.GPIO is installed by default on a Raspberry Pi and is not installable on other devices

### Environment

Create a .env file in the root of the repository and set these variables:

```env
BLYNK_TOKEN=yourToken
```

### Running the script

Run the main script:

```bash
python3 main.py
```

## Systemd service

A service is used to easily start and stop the script. It also allows to run on startup.

To create the service in systemd, copy the service file into the system folder:

```bash
cp blynk.service /lib/systemd/system/blynk.service
```

Reload the daemon to recognise the new service, then start the blynk service. Enabling the service is optional, this will make it start automatically on startup.

```bash
systemctl daemon-reload
systemctl start blynk
systemctl enable blynk
```

## Running test files

This project uses the unittest module to run tests. There are no additional packages needed to install.

Run all tests:

```bash
python3 -m unittest discover -s ./test
```

Run a single test

```bash
python3 -m unittest test.test_stepper_motor
```
