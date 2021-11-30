#!/bin/bash

#使用する低レベルランタイムを宣言
declare -a low_level_runtime=("cri-o-runc" "runsc" "crun")
#各低レベルランタイムについてコンテナを立ち上げる個数
container_num=5
#コンテナイメージの指定
container_image="busybox"
