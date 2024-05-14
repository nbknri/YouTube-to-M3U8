#! /usr/bin/python3

import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                print('https://raw.githubusercontent.com/user-name/repo-name/main/assets/info.m3u8')
                return
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
    return hd[st:].strip()

s = requests.Session()

# Iterate through each line in the channel-name.txt file
with open('../channel-name.txt') as f:
    for line in f:
        line = line.strip()
        if line.startswith('https://'):
            continue
        # Split the line into channel name, group name, logo, and tvg-id
        line_parts = line.split('|')
        ch_name = line_parts[0].strip()
        # Adjust other parts as needed...
        url = line_parts[-1].strip()
        m3u8_content = grab(url)
        with open(f'{ch_name}.m3u8', 'w') as m3u8_file:
            m3u8_file.write(m3u8_content)

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
