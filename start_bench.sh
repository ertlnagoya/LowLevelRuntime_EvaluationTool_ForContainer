#!/bin/bash

#Move to the directory which has start_bench.sh
if [ -n "${BASH_SOURCE%start_bench.sh}" ]; then
  echo "cd "${BASH_SOURCE%start_bench.sh}
  cd ${BASH_SOURCE%start_bench.sh}
fi
#Run benchmarks according to argument ($1)
if [ -z "$1" ]; then
  echo "Specify benchmark items"
elif [ -e "$1"/"$1".sh ]; then
  if [ "$1" = "syscall_collect" ] || [ "$1" = "lifecycle" ] || [ "$1" = "resource_cpu" ] || [ "$1" = "resource_memory" ] || [ "$1" = "resource_storage" ]; then
    if [ -z "$2" ]; then
      echo "Specify container image"
    else
      source "$1"/"$1".sh "$2"
      source run_bench.sh "$1"
    fi
  else
    source "$1"/"$1".sh
    source run_bench.sh "$1"
  fi
elif [ "$1" = "gompertz_cve" ]; then
  rm epss_scores*
  curl -OL https://epss.cyentia.com/epss_scores-current.csv.gz
  gunzip epss_scores*
  mv epss_scores* epss_scores.csv
  python3 "$1"/cve_collect.py
else
  echo "$1"/"$1".sh
  echo "Specify the exist benchmark item"
fi
