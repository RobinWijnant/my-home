FROM alpine

RUN apk add \
  gcc \
  python3-dev \
  py3-pip \
  musl-dev \
  linux-headers \
  git

RUN pip3 install \
  RPi.GPIO \
  python-dotenv \
  RpiMotorLib \
  adafruit-circuitpython-ads1x15 \
  paho-mqtt

WORKDIR /root

RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home

RUN chmod +x entrypoint.sh
CMD [ "/bin/sh", "-c", "./entrypoint.sh" ]