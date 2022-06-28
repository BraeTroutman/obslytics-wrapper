#!/bin/bash

source /usr/src/io/conf.env

echo "++++++++++++++++HELLO WORLD++++++++++++++++++"

obslytics export --match=$MATCH --resolution=$RESOLUTION --min-time=$MIN_TIME --max-time=$MAX_TIME --input-config-file=/usr/src/io/input-config.yaml --output-config-file=/usr/src/io/output-config.yaml

cat /usr/src/io/out.pq
