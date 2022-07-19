#!/usr/local/bin/python3

from strictyaml import load, Map, Str, Int, Seq
import os
import time

QUERY_SCHEMA = Map({
    "resolution": Str(),
    "min_time": Str(),
    "max_time": Str(),
    "matches": Seq(Str())
    })

query = {}
with open('config/query.yaml') as qfile:
    query = load(qfile.read(), QUERY_SCHEMA)
    
while True:
    for match in query['matches']:
        print(f'obslytics --match={match} --resolution={query["resolution"]}')
    time.sleep(10)

