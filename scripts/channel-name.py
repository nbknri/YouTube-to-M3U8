import requests
import os
import sys

# Function to fetch M3U8 links and create M3U8 files
def grab(url, channel_name, group_name, logo, output_folder):
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            if windows:
                link = 'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8'
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write(f'#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write(link)
                return
            os.system(f'curl "{url}" > temp.txt')
            response = ''.join(open('temp.txt').readlines())
            if '.m3u8' not in response:
                link = 'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8'
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write(f'#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write(link)
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
output_folder = '../channel'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create m3u8 playlist
master_playlist = os.path.join(output_folder, '../playlist.m3u')
with open(master_playlist, 'w') as master:
    master.write('#EXTM3U\n')

# Detect if running on Windows
windows = False
if 'win' in sys.platform:
    windows = True

# Get the list of channel names from channel-name.txt
available_channel_names = []
with open('../channel-name.txt') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if '|' in line:
            channel_info = line.split(' | ')
            name = channel_info[0]
            available_channel_names.append(name)

# Process each channel
existing_m3u8_files = [file for file in os.listdir(output_folder) if file.endswith('.m3u8')]
for m3u8_file in existing_m3u8_files:
    channel_name = os.path.splitext(m3u8_file)[0]
    if channel_name not in available_channel_names:
        os.remove(os.path.join(output_folder, m3u8_file))
        
# Process each channel in channel-name.txt
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
            grab(url, name, group_name, logo, output_folder)
            # Append channel info to master playlist
            m3u8_file = f'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/channel/{name.replace(" ", "")}.m3u8'
            with open(master_playlist, 'a') as master:
                master.write(f'#EXTINF:-1 group-title="{group_name}", tvg-logo="{logo}", {name}\n')
                master.write(f'{m3u8_file}\n')
