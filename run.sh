#!/bin/bash

while read line
do
  if [[ -z $line ]]
  then
    out=$(eval "cat <<EOF
$(</usr/src/io/output-config.yaml)
    " 2> /dev/null)
    echo "$out"
    obslytics export --match=$MATCH --resolution=$RESOLUTION --min-time=$MIN_TIME --max-time=$MAX_TIME --input-config-file=/usr/src/io/input-config.yaml --output-config="$out"
  else
    eval $line
  fi
done < /usr/src/io/conf.env

