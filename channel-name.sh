#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)

mkdir -p m3u8_files

cd scripts

while IFS= read -r line; do
    if [[ $line != https:* ]]; then
        python3 channel-name.py > "../m3u8_files/$line.m3u8"
    fi
done < ../channel-name.txt

echo m3u8 files generated
