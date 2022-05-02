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
  #resource系はすべてここでコンテナイメージを引数にとってもいいかもしれない
  if [ "$1" = "syscall_collect" ] || [ "$1" = "lifecycle" ] || [ "$1" = "resource_cpu" ] || [ "$1" = "resource_memory" ] || [ "$1" = "resource_storage" ]; then
    if [ -z "$2" ]; then
      echo "コンテナイメージを指定してください"
    else
      source "$1"/"$1".sh "$2"
      source run_bench.sh "$1"
    fi
  else
    source "$1"/"$1".sh
    source run_bench.sh "$1"
  fi
else
  echo "$1"/"$1".sh
  echo "正しいベンチマークの項目を指定してください"
fi
