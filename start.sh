#!/bin/bash
nohup python miniWEB.py $1> /tmp/miniweb.log &
sleep 1
echo 'start ok'
