FROM python:3.8-alpine

RUN apk add --update alpine-sdk

RUN apk add --no-cache -X http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  motion

WORKDIR /root
RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home/camera

RUN cp -rf ./motion /etc/motion

EXPOSE 8080 8081

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]