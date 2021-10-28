#!/bin/bash

#$1にfor文の繰り返し回数、$2にランタイム、$3にコンテナイメージを選択
for j in $(seq 1 "$1"); do
    docker run --runtime=$2 --name=$2$j $3
done
