#!/bin/bash

#メイン処理
rm -f "$1"/err_war.txt
for ((i = 0; i < ${#low_level_runtime[@]}; i++)) {
    rm -f "$1"/${low_level_runtime[i]}.txt
    if [ "$1" = "resource_memory" ]; then
        #メモリ量を測定した後、run_roop.shにてコンテナを実行
        free -s 1 -m > resource_memory/${low_level_runtime[i]}.txt &
        source run_roop.sh ${container_num} ${low_level_runtime[i]} ${container_image}
        #freeコマンドをkill
        ps_result=($(ps -C free))
        ps_id=${ps_result[4]}
        kill ${ps_id}
        source stop_rm_roop.sh ${container_num} ${low_level_runtime[i]}
    else
        for ((j = 0; j < ${container_num}; j++)) {
            docker run --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            docker stop ${low_level_runtime[i]}$j > /dev/null && docker rm ${low_level_runtime[i]}$j > /dev/null
        }
    fi
    echo ${low_level_runtime[i]} " Finish"
}

#このあと、pythonでグラフ描画処理
python3 make_graph.py "$1" ${low_level_runtime[@]}
