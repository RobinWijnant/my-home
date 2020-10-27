FROM python:3.8

RUN pip install \
  RPi.GPIO \
  python-dotenv \
  paho-mqtt \
  RpiMotorLib \
  adafruit-circuitpython-ads1x15

WORKDIR /root

RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home/roller_blind

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]