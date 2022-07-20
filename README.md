# obslytics-wrapper

A python container image wrapping the obslytics tool for pulling data from Thanos/Prometheus in a parquet format. It supports querying remote or cluster-internal prometheus remoteread or thanos storeapi endpoints for time series metrics over time, and allows for python scripting to prepocess and aggregate data for analysis.

## contains:

```
obslytics-wrapper
├── Dockerfile      -- builds python image with included obslytics binary
├── Dockerfile.comp -- builds an obslytics go image, already build and available @braet/obslytics-wrapper on dockerhub
├── obslytics	    -- modified obslytics source code to allow for bearer-auth
├── pkg		    -- modified prometheus and thanos source code
├── pyscripts	    -- python3 dependencies and scripts for prepocessing go here
├── run.sh	    -- the entrypoint for the container, runs queries and python processing
└── config	    -- contains configuration information for obslytics and run.sh
```

## configuration

```
config
├── query.yaml         -- (1)
├── input-config.yaml  -- (2)
└── output-config.yaml -- (3)
```

All of these files are compatible to be loaded as a configmap into Openshift and the deployed container can access the configuration by mounting said configmap to the /usr/src/io directory in the pod deployment.

1. query.yaml: contains config for the queries that will be run by obslytics against the Thanos or Prometheus endpoint. Specify query frequency, resolution (range of time in each query), query beginning time, query end time, as well as a list of metrics that should be pulled from the endpoint.

2. input-config.yaml shouldn't need to be changed, just edits the api endpoint to be queried for metrics. This should be the cluster-internal thanos-recieve endpoint setup by the observability operator.

3. output-config.yaml: a template file for output configuration passed to obslytics. Environment variables in this file will be evaluated/replaced with their values when loaded. Parameters in here can be changed to allow output on the local filesystem or to other object stores beyond s3.

