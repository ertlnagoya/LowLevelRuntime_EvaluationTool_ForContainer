#!/bin/bash

for ((i = 0; i < 100; i++)) {
    fio -rw=randwrite -bs=1k -size=50m -directory=./fio -direct=1 -numjobs=10 -name=file1 -ioengine=libaio &
}
