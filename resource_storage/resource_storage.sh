#!/bin/bash

#使用する低レベルランタイムを宣言
declare -a low_level_runtime=("runc" "crun" "runsc" "kata")
#各低レベルランタイムについてコンテナを立ち上げる個数
container_num=20
#コンテナイメージの指定
container_image="paipoi/sysbench_"$(uname -p)""
