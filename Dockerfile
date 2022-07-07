FROM ubuntu:latest AS prep

WORKDIR /usr/src/app

RUN apt update && apt install -y ca-certificates

RUN mkdir /usr/src/io
COPY run.sh ./
COPY target /usr/src/io

RUN chmod +x run.sh

COPY --from=braet/obslytics-wrapper /go/bin /usr/local/bin

CMD ["./run.sh"]

