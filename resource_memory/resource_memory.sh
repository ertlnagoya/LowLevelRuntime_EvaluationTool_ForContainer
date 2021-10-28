#!/bin/bash

#使用する低レベルランタイムを宣言
declare -a low_level_runtime=("runsc" "crun")
#各低レベルランタイムについてコンテナを立ち上げる個数
container_num=5
#コンテナイメージの指定
container_image="busybox"

parent_dir=$(dirname $(dirname $0))

#メモリ測定のメイン処理
for ((i = 0; i < ${#low_level_runtime[@]}; i++)) {
    #メモリ量を測定した後、run_roop.shにてコンテナを実行
    rm -f memory/${low_level_runtime[i]}.txt
    free -s 1 -m > memory/${low_level_runtime[i]}.txt &
    source ${parent_dir}/run_roop.sh ${container_num} ${low_level_runtime[i]} ${container_image}
    #freeコマンドをkill
    ps_result=($(ps -C free))
    ps_id=${ps_result[4]}
    kill ${ps_id};
    source ${parent_dir}/stop_rm_roop.sh ${container_num} ${low_level_runtime[i]}
}

#このあと、pythonでグラフ描画処理
python3 ${parent_dir}/make_graph.py memory ${low_level_runtime[@]}