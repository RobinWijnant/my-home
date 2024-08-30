FROM alpine:3.12

RUN apk add --no-cache bash curl bind-tools jq

WORKDIR /app

COPY directadmin-dynamic-dns.sh /app/directadmin-dynamic-dns.sh

CMD ["/bin/bash", "/app/directadmin-dynamic-dns.sh"]
