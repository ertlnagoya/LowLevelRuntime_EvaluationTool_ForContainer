#!/bin/bash

#$1にfor文の繰り返し回数、$2にランタイム、$3にコンテナイメージを選択
for j in $(seq 1 "$1"); do
#${@:3}にすることで、コンテナイメージとその引数を同時に取得できる
    docker run --runtime=$2 --name=$2$j ${@:3}
done
