#!/bin/bash

for ((i = 0; i < 65536; i++)) {
    touch memo_${i}.txt
    inotifyd -a memo_${i}.txt &
}