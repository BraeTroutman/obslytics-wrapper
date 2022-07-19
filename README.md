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
├── conf.env           -- (1)
├── input-config.yaml  -- (2)
└── output-config.yaml -- (3)
```

1. conf.env: a list of environment variables to use when running the container. Each block of variables is in scope for one iteration of running the obslytics tool, and remains in scope unless over written in the next iteration. Separate each set of env vars by an empty newline, as run.sh parses this file based on empty lines, loading environment variables on full lines and running obslytics on empty ones. This way, you can change the value for $MATCH (the metric to query) or any other variables you'd like to mutate each iteration. run.sh will execute one query for every empty-line separated block in this file. Make sure there is an empty line at the end of the file, or the last query will not be run. NOTE your AWS access and secret keys must be added as environment vars in this file or in output-config.yaml in order for s3 output to work.

2. input-config.yaml shouldn't need to be changed, just edits the api endpoint to be queried for metrics. This should be the cluster-internal thanos-recieve endpoint setup by the observability operator.

3. output-config.yaml: a template file for output configuration passed to obslytics. Environment variables and bash globs/inline string replacment etc will be evaluated/replaced with their values when this file is loaded. Parameters in here can be changed to allow output on the local filesystem or to other object stores beyond s3.

