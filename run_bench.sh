#!/bin/bash

#引数($1)の値に沿ってベンチマークを実行する
if [ -z "$1" ]; then
  echo "ベンチマークの項目を指定してください"
elif [ -e "$1"/"$1".sh ]; then
  source "$1"/"$1".sh
else
  echo "$1"/"$1".sh
  echo "正しいベンチマークの項目を指定してください"
fi
