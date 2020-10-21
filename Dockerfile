FROM python:3.8

RUN pip install \
  RPi.GPIO \
  python-dotenv \
  RpiMotorLib \
  adafruit-circuitpython-ads1x15 \
  paho-mqtt

WORKDIR /root

RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]