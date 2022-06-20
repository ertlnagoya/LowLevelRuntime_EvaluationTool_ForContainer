#!/bin/bash

#Declare low-level runtime
declare -a low_level_runtime=("runc" "crun" "runsc" "kata" "kata-fc")
#Number of containers to launch for each low-level runtime
container_num=10
#Specify container image
container_image="paipoi/sysbench_"$(uname -p)" sysbench --test=cpu --cpu-max-prime=20000 --num-threads=1 run"
