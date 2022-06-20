#!/bin/bash

#Adjustment-Time for gVisor and Kata that take longer to process
sleep_time=3
#Time to force rm(command) if container keeps operating
continue_time=60

rm -f "$1"/err_war.txt

#In tha case of syscall_collect, download CVE and EPSS csv firstly
if [ "$1" = "syscall_collect" ]; then
    curl -OL https://cve.mitre.org/data/downloads/allitems.csv
    rm epss_scores*
    curl -OL https://epss.cyentia.com/epss_scores-current.csv.gz
    gunzip epss_scores*
    mv epss_scores* epss_scores.csv
fi

for ((i = 0; i < ${#low_level_runtime[@]}; i++)) {
    #Remove logs for each benchmark
    rm -f "$1"/${low_level_runtime[i]}.txt
    
    #Run lifecycle benchmark
    if [ "$1" = "lifecycle" ]; then
        #Repeat for number of container_num
        for ((j = 0; j < ${container_num}; j++)) {
            echo $(($j+1))"cycle" >> lifecycle/${low_level_runtime[i]}.txt
            #Create Container
            echo "create" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker create -t --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            #Start Container
            echo "start" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker start ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            #Stop Container
            echo "stop" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker stop --time=10 ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            #Remove Container
            echo "remove" >> lifecycle/${low_level_runtime[i]}.txt
            time -p (docker rm ${low_level_runtime[i]}$j > /dev/null) &>> lifecycle/${low_level_runtime[i]}.txt
            wait $!
            echo "" >> lifecycle/${low_level_runtime[i]}.txt
            sleep ${sleep_time}
        }
    #Run resource_storage benchmark
    elif [ "$1" = "resource_storage" ]; then
        df -m / >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
        #Make for number of container_num
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
    #resource_cpu or resource_memory benchmark
    elif [ "$1" = "resource_cpu" ] || [ "$1" = "resource_memory" ]; then
        #Specify resource_cpu or resource_memory
        if [ "$1" = "resource_cpu" ]; then mpstat 1 > resource_cpu/${low_level_runtime[i]}.txt &
        elif [ "$1" = "resource_memory" ]; then free -s 1 -m > resource_memory/${low_level_runtime[i]}.txt &
        fi
        #Run container
        for ((j = 0; j < ${container_num}; j++)) {
            docker run -td --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} > /dev/null
        }
        #Kill command
        if [ "$1" = "resource_cpu" ]; then ps_result=($(ps -C mpstat))
        elif [ "$1" = "resource_memory" ]; then ps_result=($(ps -C free))
        fi
        ps_id=${ps_result[4]}
        kill ${ps_id}
        #Remove container
        for ((j = 0; j < ${container_num}; j++)) {
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
        }
        wait $!
        sleep ${sleep_time}
    #Run file_read benchmark
    elif [ "$1" = "file_rnd_read" ] ||  [ "$1" = "file_seq_read" ]; then
        #Run container
        for ((j = 0; j < ${container_num}; j++)) {
            docker run --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j paipoi/sysbench_"$(uname -p)" sh -c "sysbench --test=fileio prepare && sysbench --test=fileio --file-test-mode=$container_image --num-threads=1 run" >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            docker rm -f ${low_level_runtime[i]}$j > /dev/null
            wait $!
            sleep ${sleep_time}
        }
    #Run network benchmark
    elif [ "$1" = "network" ]; then
        #Run container as iperf host firstly
        docker run -d --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]} --ip=172.17.0.2 paipoi/iperf_"$(uname -p)" iperf -s > /dev/null
        wait $!
        sleep ${sleep_time}
        #Client processe on the host flows traffic
        for ((j = 0; j < ${container_num}; j++)) {
            iperf -f M -c 172.17.0.2 >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            sleep ${sleep_time}   
        }
        docker rm -f ${low_level_runtime[i]} > /dev/null
    #Run syscall_collect benchmark
    elif [ "$1" = "syscall_collect" ]; then
        #For reasons that I can't run sysdig in the background, start another terminal to run sysdig.
        #Filter to only syscalls for the specified in container.name
        gnome-terminal -- bash -c "sudo sysdig -w $1/${low_level_runtime[i]}.scap container.name=${low_level_runtime[i]};"
        echo ${container_image}
        #In the case of containers that repeat running, transition to the next command after continue_time-name=${low_level_runtime[i]} ${container_image} > /dev/null
        wait $!
        sudo pkill sysdig
        docker rm -f ${low_level_runtime[i]} > /dev/null
        #Get only evt.type (equivalent to a syscall) from sysdig raw data
        sysdig -r $1/${low_level_runtime[i]}.scap -p"%evt.type" > $1/${low_level_runtime[i]}.txt
        #Sort by number of syscall and name
        sort $1/${low_level_runtime[i]}.txt | uniq -c | sort -r > $1/${low_level_runtime[i]}_sort.txt
        rm $1/${low_level_runtime[i]}.txt
        wait $!
    #Run other benchmark
    else
        #Run benchmark given by the command line arguments
        for ((j = 0; j < ${container_num}; j++)) {
            docker run --runtime=${low_level_runtime[i]} --name=${low_level_runtime[i]}$j ${container_image} >> "$1"/${low_level_runtime[i]}.txt 2>> "$1"/err_war.txt
            wait $!
            #Check if the container has been finished abnormally, and if so, restart it.
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

#Drawing Graph with python
python3 make_graph.py "$1" ${container_num} ${low_level_runtime[@]}
