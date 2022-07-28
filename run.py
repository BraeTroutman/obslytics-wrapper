#!/usr/local/bin/python3

from strictyaml import load, Map, Str, Int, Seq
import pyarrow.parquet as pq
import subprocess as sub
import pandas as pd
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
    s3_resource = boto3.resource('s3', aws_access_key_id=os.environ['ACCESS'], aws_secret_access_key=os.environ['SECRET'])
    bucket = s3_resource.Bucket(output_config['storage']['config']['bucket'].data)
    key_list = [obj.key for obj in filter(lambda x: x.key != 'metrics.pq', bucket.objects.all())]
    metric_list = [item for item in map(lambda s: s.removesuffix('.pq'), key_list)]
    drop_cols = ['_sample_end', '_min_time', '_max_time', '_count', '_min', '_max']

    agg_table = []
    i = 0
    for key in key_list:
        obj_handle = bucket.Object(key)
        with io.BytesIO() as f:
           obj_handle.download_fileobj(f)
           f.seek(0)
           metric = key.removesuffix('.pq')
           table = pq.read_table(f).to_pandas().rename(columns={'_sum': metric}).drop(columns=drop_cols)
           if i == 0:
               agg_table = table.sort_values(by=['timestamp'])
           else:
               agg_table = pd.merge_asof(agg_table, table.sort_values(by=['timestamp']), on='timestamp', by='cluster', tolerance=pd.Timedelta('5s'))
           i += 1
    dup_cols_x = [item for item in filter(lambda x: '_x' in x, agg_table.columns)]
    cols = [item for item in map(lambda x: x.removesuffix('_x'), dup_cols_x)]
    dup_cols_y = [item for item in map(lambda x: x + '_y', cols)]
    x_to_norm = {x: norm for (x, norm) in zip(dup_cols_x, cols)}
    
    agg_table = agg_table.rename(columns=x_to_norm).drop(columns=dup_cols_y)
    agg_table = agg_table.loc[:,~agg_table.columns.duplicated()].copy()
    
    with io.BytesIO() as f:
        agg_table.to_parquet(f)
        bucket.upload_fileobj(f, 'metrics.pq')

    time.sleep(query['frequency_sec'].data)

