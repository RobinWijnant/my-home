# My Home

🎚 A python 3 script running on Raspberry Pi 4 that exposes handlers for Blynk.

## Features

- Roller blind doing an up/downwards motion based on:
  - a fixed position
  - a fixed time
  - sunrise & sunset

## Getting started

The following pip packages are required:

```bash
pip3 install python-dotenv blynklib RpiMotorLib RPi.GPIO
```

> **Note:** RPi.GPIO is installed by default on a Raspberry Pi and is not installable on other devices

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

Reload the deamon to recognise the new service, then start the blynk service. Enabling the service is optional, this will make it start automatically on startup.

```bash
systemctl daemon-reload
systemctl start blynk
systemctl enable blynk
```
