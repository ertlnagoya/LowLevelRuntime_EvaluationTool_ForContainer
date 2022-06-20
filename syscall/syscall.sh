#!/bin/bash

#Declare low-level runtime
declare -a low_level_runtime=("runc" "crun" "runsc" "kata" "kata-fc")
#Number of containers to launch for each low-level runtime
container_num=10
#Specify container image
container_image="paipoi/unixbench_"$(uname -p)" ./Run -v -i 10 -c 1 syscall"
