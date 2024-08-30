FROM alpine:3.20

RUN apk add --no-cache bash curl bind-tools jq

WORKDIR /app

COPY directadmin-dynamic-dns.sh /app/directadmin-dynamic-dns.sh

# Configure cron to run script every hour
RUN mkdir /etc/cron
RUN echo "0 * * * * /app/directadmin-dynamic-dns.sh" > /etc/cron/crontab
RUN echo "# empty line" >> /etc/cron/crontab

# Init cron
RUN crontab /etc/cron/crontab

CMD ["crond", "-f"]
