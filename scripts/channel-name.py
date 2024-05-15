import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url, channel_name, output_folder):
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                print('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')
                return
            #os.system(f'wget {url} -O temp.txt')
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                print('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')
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
    output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
    with open(output_file, 'w') as f:
        f.write('#EXTM3U\n')
        f.write('#EXT-X-VERSION:3\n')
        f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
        f.write(hd[st:].strip())

s = requests.Session()

# Create the "channel" folder if it doesn't exist
output_folder = 'channel'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open('../channel-name.txt') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if '|' in line:
            channel_info = line.split(' | ')
            name = channel_info[0]
            url = lines[i+1].strip()  # Get the URL from the next line
            grab(url, name, output_folder)
