#!/bin/bash

ps_result=($(ps -C free))
ps_id=${ps_result[4]}
echo ${ps_id}
#このあとkillしちまえば良い
