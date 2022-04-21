FROM alpine

COPY aircast-arm.bin /bin/aircast
RUN chmod +x /bin/aircast

ENTRYPOINT ["sh", "/bin/aircast"]
