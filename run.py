#!/usr/local/bin/python3

from strictyaml import load, Map, Str, Int, Seq
import subprocess as sub
import dateparser
import boto3
import time
import os
import io

QUERY_SCHEMA = Map({
    "resolution": Str(),
    "min_time": Str(),
    "max_time": Str(),
    "frequency_sec": Int(),
    "matches": Seq(Str())
    })

OUTPUT_CONFIG_SCHEMA = Map({
    "type": Str(),
    "path": Str(),
    "storage": Map({
        "type": Str(),
        "config": Map({
            "endpoint": Str(),
            "bucket": Str(),
            "access_key": Str(),
            "secret_key": Str()
            })
        })
    })

query = {}
output_config = ""

while True:
    with open('/usr/src/io/query.yaml') as qfile:
        query = load(qfile.read(), QUERY_SCHEMA)
    with open('/usr/src/io/output-config.yaml') as ofile:
        output_config = os.path.expandvars(ofile.read())
        output_config = load(output_config, OUTPUT_CONFIG_SCHEMA)

    min_time = dateparser.parse(query['min_time'].data).astimezone().isoformat()
    max_time = dateparser.parse(query['max_time'].data).astimezone().isoformat()
    for match in query['matches']:
        output_config['path'] = match.data.replace(':', '->') + '.pq'
        sub.run('obslytics export' \
                f' --match={match}' \
                f' --resolution={query["resolution"]}' \
                f' --min-time={min_time}' \
                f' --max-time={max_time}' \
                f' --input-config-file=/usr/src/io/input-config.yaml' \
                f' --output-config="{output_config.as_yaml()}"'
                , shell=True
                , capture_output=True)
    time.sleep(query['frequency_sec'].data)

