#!/bin/bash

# This flag 0 means option q doesnt exists
# 1 means option q exists and docker-compose command is executed
# 2 means h option is set and docker-compose command isn't executed
query_exists_flag=0

while getopts ":q:h" opt; do
  case $opt in
    q) arg_1="$OPTARG"
    query_exists_flag=1
    ;;
    h) echo "Pass query by using -q option like -q \"China;Germany\" "
    query_exists_flag=2
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    exit 1
    ;;
  esac

  case $OPTARG in
    -*) echo "Option $opt needs a valid argument"
    exit 1
    ;;
  esac
done

if [ "$query_exists_flag" = 0 ]
then
   echo "Option -q is mandatory for querying. Example ./run_pipeline.sh -q \"China;Germany\" "
   exit 1
elif [ "$query_exists_flag" = 1 ]
then
    QUERY=$arg_1 docker-compose up
fi