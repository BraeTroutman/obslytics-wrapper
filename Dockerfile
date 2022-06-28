FROM ubuntu:latest AS prep

WORKDIR /usr/src/app

RUN mkdir /usr/src/io
COPY run.sh ./
COPY target /usr/src/io

RUN chmod +x run.sh

COPY --from=braet/obslytics-wrapper /go/bin /usr/local/bin

CMD ["./run.sh"]

