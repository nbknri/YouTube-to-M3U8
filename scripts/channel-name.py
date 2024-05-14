import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url, output_dir, file_name):
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
    
    # Construct the full path for the output file
    output_file_path = os.path.join(output_dir, file_name)
    
    with open(output_file_path, 'w') as f:
        f.write('#EXTM3U\n')
        f.write('#EXT-X-VERSION:3\n')
        f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
        f.write(hd[st:].strip())

s = requests.Session()

def get_channel_names(file_path):
    channel_names = []
    with open(file_path) as f:
        for line in f:
            parts = line.split('|')
            channel_name = parts[0].strip()
            channel_names.append(channel_name)
    return channel_names

channel_names = get_channel_names('channel-name.txt')

with open('channel-name.txt') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if line.startswith('https:'):
            url = line
            output_dir = 'output_directory'  # Change this to your desired output directory
            file_name = f'{channel_names[i]}_{i+1}.m3u8'
            grab(url, output_dir, file_name)
