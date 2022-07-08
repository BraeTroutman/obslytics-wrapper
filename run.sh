#!/bin/bash

# outer loop: run thanos queries/obslytics script indefinitely
while true
do
  # inner loop: read conf.env line by line
  while read line
  do
    # if the line is empty:
    if [[ -z $line ]]
    then
      
      # load the output configuration, replacing variables with their current values in the string
      # i.e. instances of $MATCH, $ACCESS, etc are replaced by their values as output-config is loaded
      # NOTE don't change the indentation of this block, heredoc syntax is weird and will mess up yaml
      #        indentation in the variable $OUT if not fully left-aligned
      out=$(eval "cat <<EOF
$(</usr/src/io/output-config.yaml)
      " 2> /dev/null)

      # run the obslytics command to pull data with the given params and configurations
      obslytics export --match=$MATCH --resolution=$RESOLUTION \
	      --min-time=$MIN_TIME --max-time=$MAX_TIME \
	      --input-config-file=/usr/src/io/input-config.yaml --output-config="$out"
    else

      # if the line is not empty, evaluate the line (e.g. change the value of $MATCH)
      eval $line

    fi
  done < /usr/src/io/conf.env

  # process sleeps for 10 minutes before pulling data again
  echo "sleeping until: $(date --date="10 minutes")"
  sleep 600
done

