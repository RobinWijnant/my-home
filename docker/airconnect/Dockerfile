FROM ubuntu:18.04

# Add Supervisor
RUN apt-get update && apt-get install -y supervisor wget
COPY supervisord.conf /etc

# Download AirConnect
RUN wget --output-document=/bin/airupnp-x86-64 https://raw.githubusercontent.com/philippe44/AirConnect/master/bin/airupnp-arm && chmod +x /bin/airupnp
RUN wget --output-document=/bin/aircast-x86-64 https://raw.githubusercontent.com/philippe44/AirConnect/master/bin/aircast-arm && chmod +x /bin/aircast

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
