#!/bin/bash

#Declare low-level runtime
declare -a low_level_runtime=("runc" "crun" "runsc" "kata" "kata-fc")
#Number of containers to launch for each low-level runtime
container_num=10
#Specify container image
container_image="paipoi/iperf3_"$(uname -p)" iperf3 -s"