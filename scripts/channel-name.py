import requests
import os

def fetch_m3u8_link(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        for line in response.text.splitlines():
            if '.m3u8' in line:
                return line.strip()
    except requests.RequestException as e:
        print(f"Error fetching m3u8 link from {url}: {e}")
    return None

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
            
            # Fetch .m3u8 link
            m3u8_link = fetch_m3u8_link(url)
            if m3u8_link:
                output_file = os.path.join(output_folder, f'{name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write(m3u8_link)
            else:
                print(f"No .m3u8 link found for {name}. Using placeholder link.")
                m3u8_link = 'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8'
            
            # Append channel info to master playlist
            with open(master_playlist, 'a') as master:
                master.write(f'#EXTINF:-1 group-title="{group_name}" tvg-logo="{logo}", {name}\n')
                master.write(f'{m3u8_link}\n')import requests
import os

def fetch_m3u8_link(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        for line in response.text.splitlines():
            if '.m3u8' in line:
                return line.strip()
    except requests.RequestException as e:
        print(f"Error fetching m3u8 link from {url}: {e}")
    return None

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
            
            # Fetch .m3u8 link
            m3u8_link = fetch_m3u8_link(url)
            if m3u8_link:
                output_file = os.path.join(output_folder, f'{name.replace(" ", "")}.m3u8')
                with open(output_file, 'w') as f:
                    f.write('#EXTM3U\n')
                    f.write('#EXT-X-VERSION:3\n')
                    f.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
                    f.write(m3u8_link)
            else:
                print(f"No .m3u8 link found for {name}. Using placeholder link.")
                m3u8_link = 'https://raw.githubusercontent.com/nbknri/YouTube-to-M3U8/main/assets/info.m3u8'
            
            # Append channel info to master playlist
            with open(master_playlist, 'a') as master:
                master.write(f'#EXTINF:-1 group-title="{group_name}" tvg-logo="{logo}", {name}\n')
                master.write(f'{m3u8_link}\n')
