FROM python:3.10-slim-bullseye 

WORKDIR /usr/src/app

RUN apt update && apt install -y ca-certificates
ADD pyscripts pyscripts

RUN python -m pip install -r pyscripts/requirements.txt

RUN mkdir /usr/src/io
COPY run.py ./
COPY config /usr/src/io

RUN chmod +x run.py

COPY --from=braet/obslytics-wrapper /go/bin /usr/local/bin

CMD ["./run.py"]

