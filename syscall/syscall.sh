#!/bin/bash

#使用する低レベルランタイムを宣言
declare -a low_level_runtime=("runc" "crun" "runsc" "kata" "kata-fc")
#各低レベルランタイムについてコンテナを立ち上げる個数
container_num=10
#コンテナイメージの指定
container_image="paipoi/unixbench_"$(uname -p)" ./Run -v -i 10 -c 1 syscall"
