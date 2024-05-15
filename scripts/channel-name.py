import requests
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url, channel_name, output_folder):
    try:
        response = s.get(url, timeout=15).text
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        response = ""

    if '.m3u8' not in response:
        try:
            response = requests.get(url).text
        except requests.RequestException as e:
            print(f"Error fetching URL {url} with requests.get: {e}")
            response = ""

        if '.m3u8' not in response:
            print(f"Using placeholder link for {channel_name}")
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
        if 'https://' in response[end-tuner:end]:
            link = response[end-tuner:end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
            if tuner > len(response):
                print(f"Using placeholder link for {channel_name}")
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')
                return

    try:
        streams = s.get(link[start:end]).text.split('#EXT')
        hd = streams[-1].strip()
        st = hd.find('http')
        output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
        with open(output_file, 'w') as f:
            f.write('#EXTM3U\n')
            f.write('#EXT-X-VERSION:3\n')
            f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
            f.write(hd[st:].strip())
    except requests.RequestException as e:
        print(f"Error fetching stream link {link[start:end]}: {e}")
        print(f"Using placeholder link for {channel_name}")
        output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
        with open(output_file, 'w') as f:
            f.write('#EXTM3U\n')
            f.write('#EXT-X-VERSION:3\n')
            f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
            f.write('https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8')

s = requests.Session()

# Create the "channel" folder if it doesn't exist
output_folder = '../channel'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create m3u8 master playlist
master_playlist = os.path.join(output_folder, '../playlist.m3u8')
with open(master_playlist, 'w') as master:
    master.write('#EXTM3U\n')

with open('../channel-name.txt') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if '|' in line:
            channel_info = line.split(' | ')
            name = channel_info[0]
            group_name = channel_info[1]
            logo = channel_info[2]
            url = lines[i+1].strip()  # Get the URL from the next line
            grab(url, name, output_folder)
            # Append channel info to master playlist
            m3u8_file = f'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/channel/{name.replace(" ", "")}.m3u8'
            with open(master_playlist, 'a') as master:
                master.write(f'#EXTINF:-1 group-title="{group_name}" tvg-logo="{logo}", {name}\n')
                master.write(f'{m3u8_file}\n')
