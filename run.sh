#!/bin/bash

while true
do
  while read line
  do
    if [[ -z $line ]]
    then
      out=$(eval "cat <<EOF
$(</usr/src/io/output-config.yaml)
      " 2> /dev/null)
      obslytics export --match=$MATCH --resolution=$RESOLUTION --min-time=$MIN_TIME --max-time=$MAX_TIME --input-config-file=/usr/src/io/input-config.yaml --output-config="$out"
    else
      eval $line
    fi
  done < /usr/src/io/conf.env
  echo "sleeping until: $(date --date="10 minutes")"
  sleep 600
done

