#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/scripts/

python3 channel-name.py > ../channel-name1.m3u8

echo m3u8 grabbed for channel 1

python3 channel-name.py > ../channel-name2.m3u8

echo m3u8 grabbed for channel 2

python3 channel-name.py > ../channel-name3.m3u8

echo m3u8 grabbed for channel 3
