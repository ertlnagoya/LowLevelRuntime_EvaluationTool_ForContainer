#!/bin/bash

#メイン処理

#処理に時間がかかるgVisorやKataの調整用時間
sleep_time=3
#コンテナが起動し続ける場合に強制的にrmするまでの時間
continue_time=60


rm -f "$1"/err_war.txt
for ((i = 0; i < ${#low_level_runtime[@]}; i++)) {
    rm -f "$1"/${low_level_runtime[i]}.txt
    if [ "$1" = "lifecycle" ]; then
        #コンテナの1連のライフサイクルをfor文で繰り返す
        for ((j = 0; j < ${container_num}; j++)) {
            echo $(($j+1))"cycle" >> lifecycle/${low_level_runtime[i]}.txt
            echo "create" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker create -t --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            echo "start" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker start ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            echo "stop" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker stop --time=10 ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            echo "remove" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker rm ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            echo "" >> lifecycle/${low_level_runtime[i]}.txt
            sleep ${sleep_time}
        }
    elif [ "$1" = "resource_storage" ]; then
        df -m / >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
        for ((j = 0; j < ${container_num}; j++)) {
            docker run -td --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} > /dev/null
        }
        wait $!
        sleep ${sleep_time}
        df -m / >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
        for ((j = 0; j < ${container_num}; j++)) {
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
        }
        wait $!
    elif [ "$1" = "resource_cpu" ] || [ "$1" = "resource_memory" ]; then
        #測定コマンドを指定
        if [ "$1" = "resource_cpu" ]; then mpstat 1 > resource_cpu/${low_level_runtime[i]}.txt &
        elif [ "$1" = "resource_memory" ]; then free -s 1 -m > resource_memory/${low_level_runtime[i]}.txt &
        fi
        #コンテナの起動
        for ((j = 0; j < ${container_num}; j++)) {
            docker run -td --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} > /dev/null
        }
        #測定コマンドをkill
        if [ "$1" = "resource_cpu" ]; then ps_result=($(ps -C mpstat))
        elif [ "$1" = "resource_memory" ]; then ps_result=($(ps -C free))
        fi
        ps_id=${ps_result[4]}
        kill ${ps_id}
        #コンテナの削除
        for ((j = 0; j < ${container_num}; j++)) {
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
        }
        wait $!
        sleep ${sleep_time}
    elif [ "$1" = "file_rnd_read" ] ||  [ "$1" = "file_seq_read" ]; then
        for ((j = 0; j < ${container_num}; j++)) {
            docker run --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j paipoi/sysbench_"$(uname -p)" sh -c "sysbench --test=fileio prepare && sysbench --test=fileio --file-test-mode=$container_image --num-threads=1 run" >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
            wait $!
            sleep ${sleep_time}
        }
    elif [ "$1" = "network" ]; then
        docker run -d --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]} --ip=172.17.0.2 paipoi/iperf_"$(uname -p)" iperf -s > /dev/null
        wait $!
        sleep ${sleep_time}
        for ((j = 0; j < ${container_num}; j++)) {
            iperf -f M -c 172.17.0.2 >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            sleep ${sleep_time}   
        }
        docker rm -f ${low_level_runtime[i]} > /dev/null
    elif [ "$1" = "syscall_collect" ]; then #システムコールの取得処理
        gnome-terminal -- bash -c "sudo sysdig -w $1/${low_level_runtime[i]}.scap container.name=${low_level_runtime[i]};"
        echo ${container_image}
        timeout ${continue_time} docker run -it --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]} ${container_image} > /dev/null
        wait $!     
        sudo pkill sysdig
        docker rm -f ${low_level_runtime[i]} > /dev/null
        sysdig -r $1/${low_level_runtime[i]}.scap -p"%evt.type" > $1/${low_level_runtime[i]}.txt
        sort $1/${low_level_runtime[i]}.txt | uniq -c | sort -r > $1/${low_level_runtime[i]}_sort.txt
        wait $!
    else
        for ((j = 0; j < ${container_num}; j++)) {
            docker run --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            tmp="docker ps -a | grep ${low_level_runtime[i]}$j | grep 'Exited (0)'"
            if [ -z "$tmp" ]; then
                docker start ${low_level_runtime[i]}$j && docker attach ${low_level_runtime[i]}$j >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            fi
            wait $!
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
            wait $!
            sleep ${sleep_time}
        }
    fi
    echo ${low_level_runtime[i]} " Finish"
}

#このあと、pythonでグラフ描画処理
python3 make_graph.py "$1" ${container_num} ${low_level_runtime[@]}
