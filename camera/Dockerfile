# motion is only available on the testing repo on alpine edge
FROM alpine:edge

RUN apk add motion

WORKDIR /root
RUN git clone https://github.com/RobinWijnant/my-home.git
WORKDIR /root/my-home/camera

RUN cp -rf ./motion /etc/motion

EXPOSE 8080 8081

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/bin/sh", "-c", "./entrypoint.sh" ]