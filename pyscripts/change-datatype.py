#!/usr/local/bin/python3

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

df = pq.read_table(source="/usr/src/io/out.pq").to_pandas()
df['_count'] = df['_count'].astype('int64')

df.to_parquet("/usr/src/io/out.parq")

