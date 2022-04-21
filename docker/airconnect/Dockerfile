FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  libssl1.0.0 \
  libssl-dev

COPY aircast-arm.bin /bin/aircast
RUN chmod +x /bin/aircast

ENTRYPOINT ["/bin/aircast"]
