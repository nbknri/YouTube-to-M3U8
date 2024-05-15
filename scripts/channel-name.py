import requests
import os
import platform

def grab(url, channel_name, output_folder):
    session = requests.Session()
    try:
        response = session.get(url, timeout=15).text
        if '.m3u8' not in response:
            response = session.get(url).text
            if '.m3u8' not in response:
                fallback_url = 'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8'
                output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write(fallback_url)
                return
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    end_index = response.find('.m3u8') + 5
    tuner = 100
    while True:
        link = response[end_index - tuner: end_index]
        if 'https://' in link:
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5

    try:
        streams = session.get(link[start:end]).text.split('#EXT')
        hd_stream = streams[-1].strip()
        stream_start = hd_stream.find('http')
        output_file = os.path.join(output_folder, f'{channel_name.replace(" ", "")}.m3u8')
        with open(output_file, 'w') as f:
            f.write('#EXTM3U\n')
            f.write('#EXT-X-VERSION:3\n')
            f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
            f.write(hd_stream[stream_start:].strip())
    except requests.RequestException as e:
        print(f"Error fetching stream: {e}")

# Determine platform
is_windows = platform.system() == "Windows"

# Create the output folder if it doesn't exist
output_folder = 'channel'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create the master playlist file
master_playlist = os.path.join(output_folder, 'playlist.m3u8')
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
            url = lines[i + 1].strip()  # Get the URL from the next line
            grab(url, name, output_folder)
            # Append channel info to master playlist
            m3u8_file = f'channel/{name.replace(" ", "")}.m3u8'
            with open(master_playlist, 'a') as master:
                master.write(f'#EXTINF:-1 group-title="{group_name}" tvg-logo="{logo}", {name}\n')
                master.write(f'{m3u8_file}\n')
