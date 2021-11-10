#!/bin/bash

#start_bench.shファイルがある場所まで移動する
if [ -n "${BASH_SOURCE%start_bench.sh}" ]; then
  echo "cd "${BASH_SOURCE%start_bench.sh}
  cd ${BASH_SOURCE%start_bench.sh}
fi
#引数($1)の値に沿ってベンチマークを実行する
if [ -z "$1" ]; then
  echo "ベンチマークの項目を指定してください"
elif [ -e "$1"/"$1".sh ]; then
  source "$1"/"$1".sh
  source run_bench.sh "$1"
else
  echo "$1"/"$1".sh
  echo "正しいベンチマークの項目を指定してください"
fi
