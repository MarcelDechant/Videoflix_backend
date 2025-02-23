import subprocess
import os
from django.conf import settings

def convert_to_hls(instance, resolution):
    """
    Convert the video into hsl format in the given resolution.
    """
    allowed_resolutions = ['480', '720', '1080']
    if resolution not in allowed_resolutions:
        raise ValueError(f"Invalid resolution. Please choose from {allowed_resolutions}") 
    
    source = instance.video_file.path
    
    clean_title = instance.title.replace(' ', '_').lower()
    video_folder = os.path.join(settings.MEDIA_ROOT, 'videos', str(instance.pk))
    path = os.path.join(video_folder, clean_title)
    os.makedirs(video_folder, exist_ok=True)
    target = path + f'_{resolution}p.m3u8'
    
    cmd = (
        f'ffmpeg -i "{source}" -s hd{resolution} -c:v libx264 -crf 23 -c:a aac '
        f'-start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{target}"'
    )
    
    subprocess.run(cmd, shell=True)
    return target
    
    
def delete_file(file_path):
    # convert to linux path for rqworker on linux
    file_path_linux = "/mnt/" + file_path.replace("\\", "/").replace("C:","c")
    # delete file
    if os.path.isfile(file_path_linux):
        os.remove(file_path_linux)
        

def create_master_playlist(instance):
    """
    Create master playlist (master.m3u8) for hls streams.
    """
    video_folder = os.path.join(settings.MEDIA_ROOT, 'videos', str(instance.pk))
    master_playlist_path = os.path.join(video_folder, 'master.m3u8')
    
    os.makedirs(video_folder, exist_ok=True)
    
    clean_title = instance.title.replace(' ', '_').lower()
    playlist_content = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        "#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360",
        f"{clean_title}_480p.m3u8",
        "#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=1280x720",
        f"{clean_title}_720p.m3u8",
        "#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080",
        f"{clean_title}_1080p.m3u8",
    ]
    
    with open(master_playlist_path, 'w') as master_playlist_file:
        for line in playlist_content:
            master_playlist_file.write(line + "\n")
            
