#! /usr/bin/python3

import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url, channel_name):
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
    with open(f'../{channel_name}.m3u8', 'w') as f:
        f.write('#EXTM3U\n')
        f.write('#EXT-X-VERSION:3\n')
        f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
        f.write(hd[st:].strip())

s = requests.Session()
with open('../channel-name.txt') as f:
    lines = f.readlines()
    for line in lines[2:]:
        if line.strip() and not line.startswith('~~'):
            parts = line.strip().split('|')
            if len(parts) >= 2:  # Ensure there are at least two parts
                channel_name = parts[0].strip()
                url = parts[1].strip()  # Use the second part for URL
                if url.startswith('https:'):
                    grab(url, channel_name)
