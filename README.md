# My Home

🎚 Python 3 scripts to run in a docker image next to Home Assistant on a Raspberry Pi 4.

- Adjustable roller blind height
- 433Mhz listener for the doorbell button

## Docker config in Portainer (in Home Assistant)

### Creating the image

1. Go to images and click the 'build new image' button.
1. Enter the name for the image
1. Select a docker file from this repo
1. Build the image

### Creating the container

1. Select the image you previously created
1. Uncheck 'Always pull the image'
1. In the 'Command and logging' tab, check the 'Interactive & TTY' console
1. In the 'Env' tab, add the env variables
1. In the 'Runtime & resources' tab, check Privileged mode (to have access to GPIO and other devices)
1. Deploy the container

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
