#!/bin/bash

#$1にfor文の繰り返し回数、$2にランタイムを選択
for j in $(seq 1 "$1"); do
    docker stop $2$j > /dev/null
    docker rm $2$j > /dev/null
done
