#! /usr/bin/python3

import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url, channel_name, output_file):
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                print('https://raw.githubusercontent.com/user-name/repo-name/main/assets/info.m3u8')
                return
            #os.system(f'wget {url} -O temp.txt')
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                print('https://raw.githubusercontent.com/user-name/repo-name/main/assets/info.m3u8')
                return
    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
    streams = s.get(link[start:end]).text.split('#EXT')
    hd = streams[-1].strip()
    st = hd.find('http')
    with open(output_file, 'w') as f:
        f.write('#EXTM3U\n')
        f.write('#EXT-X-VERSION:3\n')
        f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
        f.write(hd[st:].strip())

s = requests.Session()
with open('../channel-name.txt') as f:
    channel_info = []
    for line in f:
        line = line.strip()
        if line:
            channel_info.append(line.split(' | '))

for i, (name, group_name, logo, tvg_id) in enumerate(channel_info):
    url = channel_info[i+1][0] if i < len(channel_info) - 1 else None
    output_file = f'../{name.replace(" ", "")}.m3u8'
    grab(url, name, output_file)
