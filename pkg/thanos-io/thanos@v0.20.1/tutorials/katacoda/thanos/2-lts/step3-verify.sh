#!/usr/bin/env bash

curl -s 127.0.0.1:9090/metrics >/dev/null || exit 1
curl -s 127.0.0.1:19090/metrics >/dev/null || exit 1
curl -s 127.0.0.1:9091/metrics >/dev/null || exit 1

curl -s 127.0.0.1:19090/metrics >/dev/null || exit 1

curl -s 127.0.0.1:19091/metrics >/dev/null || exit 1

echo '"done"'
