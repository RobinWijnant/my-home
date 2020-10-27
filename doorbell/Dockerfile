FROM python:3.8

RUN pip install \
  RPi.GPIO \
  python-dotenv \
  paho-mqtt \
  rpi-rf

WORKDIR /root

RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home/doorbell

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]