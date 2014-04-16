#!/bin/bash

mkdir -p logs/
nohup python miniWEB.py > ./logs/larryqq.log &
sleep 1
echo 'start ok' 
