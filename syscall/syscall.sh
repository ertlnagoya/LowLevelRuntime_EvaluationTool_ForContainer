#!/bin/bash

#使用する低レベルランタイムを宣言
declare -a low_level_runtime=("runsc" "crun")
#各低レベルランタイムについてコンテナを立ち上げる個数
container_num=2
#コンテナイメージの指定
container_image="paipoi/unixbench2"

parent_dir=$(dirname $(dirname $0))

#システムコールscoreのメイン処理
for ((i = 0; i < ${#low_level_runtime[@]}; i++)) {
    rm -f syscall/${low_level_runtime[i]}.txt
    rm -f syscall/err_war.txt
    source ${parent_dir}/run_roop.sh ${container_num} ${low_level_runtime[i]} ${container_image} > syscall/${low_level_runtime[i]}.txt 2> syscall/err_war.txt
    source ${parent_dir}/stop_rm_roop.sh ${container_num} ${low_level_runtime[i]}
}

#このあと、pythonでグラフ描画処理
python3 ${parent_dir}/make_graph.py syscall ${low_level_runtime[@]}
